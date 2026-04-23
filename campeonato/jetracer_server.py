#!/usr/bin/env python3
"""
JetRacer Robomaster TT - Servidor de Control de Movimiento
==========================================================
Recibe comandos HTTP desde la página web del kiosko táctil
y los traduce a comandos de movimiento para el robot via WiFi.

Requisitos:
    pip install flask flask-cors robomaster

Uso:
    1. Conectar el PC a la red WiFi del Robomaster TT
       (SSID por defecto: "Robomaster_XXXXXX")
    2. Ejecutar: python jetracer_server.py
    3. Abrir la página web en Chrome a pantalla completa

Configuración:
    - El servidor Flask escucha en 0.0.0.0:5000
    - La IP del robot por defecto es 192.168.2.1
    - Ajusta ROBOT_IP si tu red es diferente
"""

import time
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

# ─── Configuración ───────────────────────────────────────────────────────────

ROBOT_IP   = "192.168.2.1"   # IP del Robomaster TT en modo AP directo
ROBOT_PORT = 10010            # Puerto SDK del robot
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

# Velocidad de movimiento (mm/s) y duración (segundos)
SPEED      = 0.5              # m/s para movimiento recto
TURN_ANGLE = 30               # grados para giro diagonal
MOVE_DIST  = 0.5              # metros por comando

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# ─── Inicialización del robot ─────────────────────────────────────────────────

robot = None

def init_robot():
    """Conecta con el Robomaster TT via SDK."""
    global robot
    try:
        from robomaster import robot as rm_robot
        robot = rm_robot.Robot()
        robot.initialize(conn_type="sta", proto_type="udp")
        log.info(f"✅ Robot conectado correctamente en {ROBOT_IP}")
        # Activar modo de movimiento libre
        robot.chassis.drive_speed(x=0, y=0, z=0)
        return True
    except ImportError:
        log.warning("⚠️  SDK de Robomaster no instalado. Ejecutando en modo SIMULACIÓN.")
        log.warning("    Instala con: pip install robomaster")
        return False
    except Exception as e:
        log.error(f"❌ Error al conectar con el robot: {e}")
        log.warning("    Ejecutando en modo SIMULACIÓN.")
        return False

def send_move(x: float, y: float, z: float, duration: float = 1.0):
    """
    Envía comando de movimiento al robot.

    Args:
        x: velocidad adelante/atrás  (+adelante, -atrás) en m/s
        y: velocidad lateral         (+izquierda, -derecha) en m/s
        z: velocidad de giro         (+antihorario, -horario) en °/s
        duration: tiempo en segundos que se mantiene el movimiento
    """
    if robot:
        try:
            robot.chassis.drive_speed(x=x, y=y, z=z)
            time.sleep(duration)
            robot.chassis.drive_speed(x=0, y=0, z=0)
            log.info(f"🤖 Movimiento: x={x}, y={y}, z={z} durante {duration}s")
        except Exception as e:
            log.error(f"❌ Error enviando comando: {e}")
    else:
        # Modo simulación
        log.info(f"🔵 [SIMULACIÓN] Movimiento: x={x:.2f}, y={y:.2f}, z={z:.2f} durante {duration}s")

# ─── Flask App ────────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)  # Permite peticiones desde la página web en cualquier origen

# ─── Rutas de movimiento ──────────────────────────────────────────────────────

@app.route("/move/forward", methods=["POST"])
def move_forward():
    """Avanzar recto hacia adelante."""
    send_move(x=SPEED, y=0, z=0)
    return jsonify({"status": "ok", "action": "forward"})


@app.route("/move/backward", methods=["POST"])
def move_backward():
    """Retroceder recto hacia atrás."""
    send_move(x=-SPEED, y=0, z=0)
    return jsonify({"status": "ok", "action": "backward"})


@app.route("/move/forward-left", methods=["POST"])
def move_forward_left():
    """Avanzar en diagonal hacia adelante-izquierda."""
    send_move(x=SPEED, y=SPEED * 0.7, z=0)
    return jsonify({"status": "ok", "action": "forward-left"})


@app.route("/move/forward-right", methods=["POST"])
def move_forward_right():
    """Avanzar en diagonal hacia adelante-derecha."""
    send_move(x=SPEED, y=-SPEED * 0.7, z=0)
    return jsonify({"status": "ok", "action": "forward-right"})


@app.route("/move/backward-left", methods=["POST"])
def move_backward_left():
    """Retroceder en diagonal hacia atrás-izquierda."""
    send_move(x=-SPEED, y=SPEED * 0.7, z=0)
    return jsonify({"status": "ok", "action": "backward-left"})


@app.route("/move/backward-right", methods=["POST"])
def move_backward_right():
    """Retroceder en diagonal hacia atrás-derecha."""
    send_move(x=-SPEED, y=-SPEED * 0.7, z=0)
    return jsonify({"status": "ok", "action": "backward-right"})


@app.route("/stop", methods=["POST"])
def stop():
    """Detener el robot."""
    if robot:
        try:
            robot.chassis.drive_speed(x=0, y=0, z=0)
        except Exception as e:
            log.error(f"❌ Error al detener: {e}")
    log.info("🛑 Robot detenido")
    return jsonify({"status": "ok", "action": "stop"})


@app.route("/status", methods=["GET"])
def status():
    """Comprueba si el servidor y el robot están listos."""
    robot_connected = robot is not None
    return jsonify({
        "server": "running",
        "robot_connected": robot_connected,
        "robot_ip": ROBOT_IP,
        "mode": "real" if robot_connected else "simulation"
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "JetRacer Robomaster TT - Servidor de Control",
        "endpoints": [
            "POST /move/forward",
            "POST /move/backward",
            "POST /move/forward-left",
            "POST /move/forward-right",
            "POST /move/backward-left",
            "POST /move/backward-right",
            "POST /stop",
            "GET  /status"
        ]
    })


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("=" * 60)
    log.info("  🤖 JetRacer Robomaster TT - Servidor de Control")
    log.info("=" * 60)
    log.info(f"  Robot IP   : {ROBOT_IP}")
    log.info(f"  Servidor   : http://{SERVER_HOST}:{SERVER_PORT}")
    log.info(f"  Velocidad  : {SPEED} m/s")
    log.info("=" * 60)

    connected = init_robot()

    if not connected:
        log.warning("🟡 Modo SIMULACIÓN activo — los comandos se mostrarán en consola")
        log.warning("   Para usar el robot real, instala el SDK y conecta al WiFi del robot")

    log.info("🚀 Servidor listo. Abre la página web en el kiosko.")
    log.info("   Presiona Ctrl+C para detener.\n")

    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
