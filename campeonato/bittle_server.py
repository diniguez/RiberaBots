"""
bittle_server.py
----------------
Servidor Flask que recibe comandos de movimiento desde la página web
y los envía al robot Petoi Bittle a través de su conexión WiFi.

Uso:
    pip install flask flask-cors requests
    python bittle_server.py

Configura la IP del Bittle en la variable BITTLE_IP antes de ejecutar.
"""

import socket
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Configuración ─────────────────────────────────────────────────────────────

BITTLE_IP   = "192.168.1.100"   # ← Cambia esto por la IP de tu Bittle
BITTLE_PORT = 8888              # Puerto UDP por defecto del Bittle
SERVER_HOST = "0.0.0.0"        # Escucha en todas las interfaces
SERVER_PORT = 5000              # Puerto del servidor Flask

# ── Mapa de comandos Bittle (protocolo serial/WiFi) ───────────────────────────
# El Bittle usa comandos de texto enviados por UDP o TCP.
# Referencia: https://docs.petoi.com/apis/serial-protocol

COMMANDS = {
    "forward":  "kwkF",   # Caminar hacia adelante
    "backward": "kbk",    # Caminar hacia atrás
    "left":     "kwkL",   # Caminar hacia la izquierda
    "right":    "kwkR",   # Caminar hacia la derecha
    "stop":     "d",      # Descanso / parar
    "balance":  "balance",# Postura de equilibrio
}

# ── Inicialización Flask ──────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen (página web local)

# Socket UDP reutilizable
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

# ── Helpers ───────────────────────────────────────────────────────────────────

def send_to_bittle(command: str) -> dict:
    """Envía un comando al Bittle por UDP y retorna estado."""
    try:
        message = command.encode("utf-8")
        sock.sendto(message, (BITTLE_IP, BITTLE_PORT))
        print(f"[BITTLE] Enviado: {command!r} → {BITTLE_IP}:{BITTLE_PORT}")
        return {"success": True, "command": command}
    except socket.timeout:
        print(f"[BITTLE] Timeout enviando: {command!r}")
        return {"success": False, "error": "Timeout: el Bittle no respondió"}
    except Exception as e:
        print(f"[BITTLE] Error: {e}")
        return {"success": False, "error": str(e)}


# ── Rutas de la API ───────────────────────────────────────────────────────────

@app.route("/move/<direction>", methods=["POST", "GET"])
def move(direction: str):
    """
    Envía un comando de movimiento al Bittle.

    Direcciones válidas: forward, backward, left, right
    Ejemplo: POST /move/forward
    """
    direction = direction.lower().strip()

    if direction not in COMMANDS:
        return jsonify({
            "success": False,
            "error": f"Dirección desconocida: '{direction}'. "
                     f"Opciones: {list(COMMANDS.keys())}"
        }), 400

    result = send_to_bittle(COMMANDS[direction])
    status_code = 200 if result["success"] else 503
    return jsonify(result), status_code


@app.route("/stop", methods=["POST", "GET"])
def stop():
    """Detiene el movimiento del Bittle."""
    result = send_to_bittle(COMMANDS["stop"])
    status_code = 200 if result["success"] else 503
    return jsonify(result), status_code


@app.route("/status", methods=["GET"])
def status():
    """Comprueba si el servidor está activo."""
    return jsonify({
        "server": "online",
        "bittle_ip": BITTLE_IP,
        "bittle_port": BITTLE_PORT,
        "available_commands": list(COMMANDS.keys())
    })


@app.route("/config", methods=["POST"])
def config():
    """
    Actualiza la IP del Bittle en tiempo de ejecución.
    Body JSON: { "ip": "192.168.x.x", "port": 8888 }
    """
    global BITTLE_IP, BITTLE_PORT
    data = request.get_json(silent=True) or {}

    if "ip" in data:
        BITTLE_IP = data["ip"]
    if "port" in data:
        BITTLE_PORT = int(data["port"])

    return jsonify({
        "success": True,
        "bittle_ip": BITTLE_IP,
        "bittle_port": BITTLE_PORT
    })


# ── Punto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  🐕 Servidor de control Petoi Bittle")
    print(f"  Bittle IP   : {BITTLE_IP}:{BITTLE_PORT}")
    print(f"  Servidor    : http://{SERVER_HOST}:{SERVER_PORT}")
    print("  Endpoints   : /move/<forward|backward|left|right>")
    print("                /stop   /status   /config")
    print("=" * 60)

    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=False,
        threaded=True
    )
