#!/usr/bin/env python3
"""
jetracer_server.py
==================
Servidor HTTP que recibe comandos de movimiento desde la página web
y los publica como mensajes ROS al JetRacer Jetson Nano ROS AI Kit.

Requisitos:
    pip install flask flask-cors rospy geometry-msgs

Uso:
    1. Asegúrate de que ROS está corriendo en el JetRacer y el master está accesible.
    2. Ejecuta este script en el PC o directamente en el JetRacer:
           python3 jetracer_server.py
    3. El servidor escucha en el puerto 5000 de todas las interfaces (0.0.0.0).
    4. La página web debe apuntar a http://<IP_DEL_SERVIDOR>:5000

Variables de entorno opcionales:
    JETRACER_HOST   IP en la que escucha el servidor  (default: 0.0.0.0)
    JETRACER_PORT   Puerto del servidor HTTP           (default: 5000)
    ROS_MASTER_URI  URI del master ROS                (default: http://localhost:11311)
    CMD_VEL_TOPIC   Topic de velocidad                (default: /cmd_vel)
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Configuración ──────────────────────────────────────────────────────────────
HOST            = os.getenv("JETRACER_HOST", "0.0.0.0")
PORT            = int(os.getenv("JETRACER_PORT", 5000))
CMD_VEL_TOPIC   = os.getenv("CMD_VEL_TOPIC", "/cmd_vel")
ROS_MASTER_URI  = os.getenv("ROS_MASTER_URI", "http://localhost:11311")

# Velocidades (m/s y rad/s) — ajusta según el comportamiento deseado
LINEAR_SPEED    = 0.3   # velocidad lineal base
ANGULAR_SPEED   = 0.6   # velocidad angular para giros
STOP_DURATION   = 0.0   # duración del comando (0 = hasta nuevo comando)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── ROS setup (opcional: si no hay ROS disponible, se usa modo simulado) ───────
try:
    import rospy
    from geometry_msgs.msg import Twist

    rospy.init_node("jetracer_web_controller", anonymous=True, disable_signals=True)
    pub = rospy.Publisher(CMD_VEL_TOPIC, Twist, queue_size=10)
    ROS_AVAILABLE = True
    log.info("✅  ROS disponible. Publicando en topic: %s", CMD_VEL_TOPIC)
except Exception as exc:
    ROS_AVAILABLE = False
    log.warning("⚠️  ROS no disponible (%s). Ejecutando en modo simulado (solo logs).", exc)


def send_twist(linear_x: float, angular_z: float) -> None:
    """Publica un mensaje Twist o lo simula si ROS no está disponible."""
    if ROS_AVAILABLE:
        msg = Twist()
        msg.linear.x  = linear_x
        msg.angular.z = angular_z
        pub.publish(msg)
    log.info("CMD → linear.x=%.2f  angular.z=%.2f", linear_x, angular_z)


# ── Mapa de comandos ───────────────────────────────────────────────────────────
# Cada comando define (linear_x, angular_z)
COMMANDS: dict[str, tuple[float, float]] = {
    "forward":       ( LINEAR_SPEED,  0.0),
    "backward":      (-LINEAR_SPEED,  0.0),
    "forward_left":  ( LINEAR_SPEED,  ANGULAR_SPEED),
    "forward_right": ( LINEAR_SPEED, -ANGULAR_SPEED),
    "backward_left": (-LINEAR_SPEED, -ANGULAR_SPEED),
    "backward_right":(-LINEAR_SPEED,  ANGULAR_SPEED),
    "stop":          ( 0.0,           0.0),
}

# ── Flask app ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen (necesario para el kiosco)


@app.route("/move", methods=["POST"])
def move():
    """
    Endpoint principal.

    Body JSON esperado:
        { "command": "<nombre_del_comando>" }

    Respuesta JSON:
        { "status": "ok", "command": "...", "linear_x": 0.3, "angular_z": 0.0 }
    """
    data = request.get_json(silent=True) or {}
    command = data.get("command", "").strip().lower()

    if command not in COMMANDS:
        valid = list(COMMANDS.keys())
        return jsonify({"status": "error", "message": f"Comando desconocido. Válidos: {valid}"}), 400

    linear_x, angular_z = COMMANDS[command]
    send_twist(linear_x, angular_z)

    return jsonify({
        "status":    "ok",
        "command":   command,
        "linear_x":  linear_x,
        "angular_z": angular_z,
    }), 200


@app.route("/stop", methods=["POST", "GET"])
def stop():
    """Detiene el robot inmediatamente."""
    send_twist(0.0, 0.0)
    return jsonify({"status": "ok", "command": "stop"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health-check para verificar que el servidor está vivo."""
    return jsonify({
        "status":        "ok",
        "ros_available": ROS_AVAILABLE,
        "topic":         CMD_VEL_TOPIC,
        "commands":      list(COMMANDS.keys()),
    }), 200


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("🚗  JetRacer Web Controller iniciando en http://%s:%d", HOST, PORT)
    log.info("📡  ROS Master: %s", ROS_MASTER_URI)
    log.info("📋  Comandos disponibles: %s", list(COMMANDS.keys()))

    try:
        app.run(host=HOST, port=PORT, debug=False, threaded=True)
    except KeyboardInterrupt:
        log.info("🛑  Servidor detenido por el usuario.")
        if ROS_AVAILABLE:
            send_twist(0.0, 0.0)  # Seguridad: detener el robot al salir
        sys.exit(0)
