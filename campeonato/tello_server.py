"""
Servidor Flask para controlar el dron DJI RoboMaster TT Tello
Se comunica con el dron via UDP y expone una API REST que consume la página web.

Requisitos:
    pip install flask flask-cors

Uso:
    1. Conectar el PC a la red WiFi del Tello (TELLO-XXXXXX)
    2. Ejecutar: python tello_server.py
    3. Abrir tello_control.html en Chrome
"""

import socket
import threading
import time
import logging
from flask import Flask, jsonify
from flask_cors import CORS

# ─── Configuración ────────────────────────────────────────────────────────────

TELLO_IP   = "192.168.10.1"
TELLO_PORT = 8889
LOCAL_PORT = 9000          # Puerto local para recibir respuestas del dron

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

MOVE_DISTANCE_CM = 50      # Distancia de avance en centímetros (20–500)
ROTATE_DEGREES   = 90      # Grados de giro (1–360)
SPEED_CM_S       = 50      # Velocidad (10–100 cm/s)

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Clase Tello ──────────────────────────────────────────────────────────────

class Tello:
    """Wrapper mínimo para comunicarse con el Tello vía UDP."""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", LOCAL_PORT))
        self.sock.settimeout(5)
        self.address = (TELLO_IP, TELLO_PORT)
        self.last_response = ""
        self._start_receiver()

    # ── Hilo receptor ────────────────────────────────────────────────────────

    def _start_receiver(self):
        t = threading.Thread(target=self._receive_loop, daemon=True)
        t.start()

    def _receive_loop(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                self.last_response = data.decode("utf-8").strip()
                log.info("Tello → %s", self.last_response)
            except socket.timeout:
                pass
            except Exception as exc:
                log.warning("Error en receptor: %s", exc)

    # ── Envío de comandos ─────────────────────────────────────────────────────

    def send(self, command: str) -> dict:
        """Envía un comando al dron y devuelve un dict con el resultado."""
        log.info("Enviando: %s", command)
        try:
            self.sock.sendto(command.encode("utf-8"), self.address)
            # Esperar respuesta hasta 5 s
            deadline = time.time() + 5
            while time.time() < deadline:
                if self.last_response:
                    resp = self.last_response
                    self.last_response = ""
                    ok = resp.lower() == "ok"
                    return {"success": ok, "response": resp, "command": command}
                time.sleep(0.05)
            return {"success": False, "response": "timeout", "command": command}
        except Exception as exc:
            log.error("Error enviando '%s': %s", command, exc)
            return {"success": False, "response": str(exc), "command": command}

    # ── Comandos de alto nivel ────────────────────────────────────────────────

    def enable_sdk(self):
        return self.send("command")

    def takeoff(self):
        return self.send("takeoff")

    def land(self):
        return self.send("land")

    def move_forward(self, cm: int = MOVE_DISTANCE_CM):
        return self.send(f"forward {cm}")

    def rotate_left(self, deg: int = ROTATE_DEGREES):
        return self.send(f"ccw {deg}")

    def rotate_right(self, deg: int = ROTATE_DEGREES):
        return self.send(f"cw {deg}")

    def set_speed(self, speed: int = SPEED_CM_S):
        return self.send(f"speed {speed}")


# ─── Flask app ────────────────────────────────────────────────────────────────

app   = Flask(__name__)
CORS(app)          # Permite peticiones desde el HTML (mismo equipo o red local)
tello = Tello()


def _init_tello():
    """Inicializa el SDK y configura la velocidad al arrancar."""
    log.info("Iniciando SDK del Tello…")
    r = tello.enable_sdk()
    if r["success"]:
        log.info("SDK activado. Configurando velocidad a %d cm/s…", SPEED_CM_S)
        tello.set_speed(SPEED_CM_S)
    else:
        log.warning("No se pudo activar el SDK: %s", r["response"])


# ── Rutas ─────────────────────────────────────────────────────────────────────

@app.route("/takeoff",  methods=["POST"])
def route_takeoff():
    jsonify(tello.takeoff())
    return jsonify(tello.move_up(100))

@app.route("/land",     methods=["POST"])
def route_land():
    return jsonify(tello.land())

@app.route("/forward",  methods=["POST"])
def route_forward():
    return jsonify(tello.move_forward())

@app.route("/left",     methods=["POST"])
def route_left():
    return jsonify(tello.rotate_left())

@app.route("/right",    methods=["POST"])
def route_right():
    return jsonify(tello.rotate_right())

@app.route("/status",   methods=["GET"])
def route_status():
    """Endpoint de comprobación: devuelve si el servidor está vivo."""
    return jsonify({"status": "online", "server": "Tello Controller"})


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    _init_tello()
    log.info("Servidor escuchando en http://%s:%d", SERVER_HOST, SERVER_PORT)
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
