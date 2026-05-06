#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JetRacer Robot Control Server
Compatible con Python 2.7.17
Recibe comandos HTTP desde la pagina web y los publica como mensajes ROS
al robot JetRacer Jetson Nano AI Kit via WiFi.
"""

from __future__ import print_function
import json
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn

# ── Configuracion ──────────────────────────────────────────────────────────────
HOST = '0.0.0.0'
PORT = 8080

# Velocidades (ajustar segun el robot)
THROTTLE_FWD  =  0.3   # aceleracion hacia delante
THROTTLE_BACK = -0.3   # aceleracion hacia atras
STEERING_LEFT = -0.4   # angulo izquierda
STEERING_RIGHT =  0.4  # angulo derecha
STEERING_STR  =  0.0   # recto

# Intenta importar rospy; si no esta disponible corre en modo simulacion
try:
    import rospy
    from std_msgs.msg import Float32
    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False
    print("[WARN] rospy no encontrado. Ejecutando en modo simulacion (sin ROS).")

# ── ROS Publisher ──────────────────────────────────────────────────────────────
class RobotController(object):
    def __init__(self):
        self.throttle = 0.0
        self.steering = 0.0
        if ROS_AVAILABLE:
            rospy.init_node('jetracer_web_controller', anonymous=True)
            self.pub_throttle = rospy.Publisher('/jetracer/throttle', Float32, queue_size=1)
            self.pub_steering = rospy.Publisher('/jetracer/steering', Float32, queue_size=1)
            print("[ROS] Nodo inicializado. Publicando en /jetracer/throttle y /jetracer/steering")

    def send(self, throttle, steering):
        self.throttle = throttle
        self.steering = steering
        if ROS_AVAILABLE:
            self.pub_throttle.publish(Float32(throttle))
            self.pub_steering.publish(Float32(steering))
        print("[CMD] throttle={:.2f}  steering={:.2f}".format(throttle, steering))

# Instancia global del controlador
robot = RobotController()

# ── Tabla de comandos ──────────────────────────────────────────────────────────
COMMANDS = {
    'forward':       (THROTTLE_FWD,  STEERING_STR),
    'backward':      (THROTTLE_BACK, STEERING_STR),
    'stop':          (0.0,           0.0),
    'forward_left':  (THROTTLE_FWD,  STEERING_LEFT),
    'forward_right': (THROTTLE_FWD,  STEERING_RIGHT),
    'backward_left': (THROTTLE_BACK, STEERING_LEFT),
    'backward_right':(THROTTLE_BACK, STEERING_RIGHT),
}

# ── HTTP Handler ───────────────────────────────────────────────────────────────
class CommandHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Silencia el log por defecto de BaseHTTPServer (opcional)
        pass

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        # CORS: permite peticiones desde cualquier origen (pagina web local)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        # Preflight CORS
        self._set_headers(200)

    def do_GET(self):
        if self.path == '/status':
            self._set_headers(200)
            body = json.dumps({
                'status': 'ok',
                'ros': ROS_AVAILABLE,
                'throttle': robot.throttle,
                'steering': robot.steering,
            })
            self.wfile.write(body.encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/command':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode('utf-8'))
                cmd = data.get('command', '').strip().lower()
                if cmd in COMMANDS:
                    throttle, steering = COMMANDS[cmd]
                    robot.send(throttle, steering)
                    self._set_headers(200)
                    resp = json.dumps({'ok': True, 'command': cmd,
                                       'throttle': throttle, 'steering': steering})
                else:
                    self._set_headers(400)
                    resp = json.dumps({'ok': False, 'error': 'Comando desconocido: ' + cmd,
                                       'valid': list(COMMANDS.keys())})
                self.wfile.write(resp.encode('utf-8'))
            except (ValueError, KeyError) as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Servidor HTTP multi-hilo para manejar varias peticiones simultaneas."""
    daemon_threads = True


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    server = ThreadedHTTPServer((HOST, PORT), CommandHandler)
    print("=" * 60)
    print("  JetRacer Web Controller Server")
    print("  Escuchando en http://{}:{}".format(HOST, PORT))
    print("  ROS disponible: {}".format(ROS_AVAILABLE))
    print("  Endpoints:")
    print("    GET  /status       -> estado actual del robot")
    print("    POST /command      -> enviar comando (JSON: {command: '...'} )")
    print("  Comandos validos: {}".format(', '.join(COMMANDS.keys())))
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido.")
        robot.send(0.0, 0.0)  # Seguridad: detener robot al cerrar
