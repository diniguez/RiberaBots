#!/usr/bin/env python3
"""
jetracer_server.py
==================
Servidor HTTP que recibe comandos de movimiento desde la página web
y los publica como mensajes ROS al JetRacer Jetson Nano ROS AI Kit.

Instalación de dependencias:
    pip install flask flask-cors rospy

    NOTA: geometry_msgs NO es una librería de pip. Es un paquete ROS que viene
    incluido con la instalación de ROS (ros-noetic-geometry-msgs o similar).
    Este script construye el mensaje Twist manualmente mediante un diccionario
    serializado a JSON, evitando la importación directa de geometry_msgs.

Uso:
    1. Ejecuta este script EN EL JETRACER (Jetson Nano):
           python3 jetracer_server.py
    2. El servidor queda escuchando en el puerto 5000.
    3. Abre la página web en el kiosco y apúntala a la IP del JetRacer.
"""

# ==============================================================================
#  🌐  CONFIGURACIÓN DE RED — EDITA AQUÍ
# ==============================================================================

# IP del JetRacer (Jetson Nano) en la red WiFi.
# Es la dirección que debes escribir también en la página web (campo "Servidor").
# Ejemplo: "192.168.1.50"  →  la web apuntará a http://192.168.1.50:5000
JETRACER_IP   = "192.168.50.23"   # <-- CAMBIA ESTO por la IP real del JetRacer

# Puerto en el que escucha este servidor HTTP.
# Debe coincidir con el puerto que pongas en la URL de la página web.
SERVER_PORT   = 5000              # <-- cambia si el puerto está ocupado

# URI del master ROS que corre en el JetRacer.
# Si ejecutas este script EN el propio JetRacer, deja "localhost".
# Si lo ejecutas en un PC externo, pon la IP del JetRacer aquí también.
ROS_MASTER_URI = f"http://localhost:11311"

# Topic ROS al que se publican los comandos de velocidad.
CMD_VEL_TOPIC  = "/cmd_vel"       # estándar en ROS para robots de tracción

# ==============================================================================
#  🚗  PARÁMETROS DE MOVIMIENTO — ajusta a tu robot
# ==============================================================================

LINEAR_SPEED  = 0.3   # m/s   — velocidad lineal (adelante/atrás)
ANGULAR_SPEED = 0.6   # rad/s — velocidad angular (izquierda/derecha)

# ==============================================================================
#  ⚙️  NO ES NECESARIO EDITAR NADA POR DEBAJO DE ESTA LÍNEA
# ==============================================================================

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Exportar ROS_MASTER_URI al entorno para que rospy lo tome automáticamente
os.environ.setdefault("ROS_MASTER_URI", ROS_MASTER_URI)

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── ROS setup ─────────────────────────────────────────────────────────────────
# geometry_msgs NO se importa como paquete pip independiente: viene incluido
# con ROS (ros-noetic-geometry-msgs).  Lo importamos dentro del try para que,
# si ROS no está instalado, el servidor arranque igualmente en modo simulado.

ROS_AVAILABLE  = False
pub            = None
_make_twist_fn = None


def _make_twist(linear_x: float, angular_z: float):
    """Construye un mensaje Twist con los valores indicados."""
    msg = _TwistClass()
    msg.linear.x  = linear_x
    msg.angular.z = angular_z
    return msg


try:
    import rospy
    from geometry_msgs.msg import Twist as _TwistClass

    rospy.init_node("jetracer_web_controller", anonymous=True, disable_signals=True)
    pub = rospy.Publisher(CMD_VEL_TOPIC, _TwistClass, queue_size=10)

    ROS_AVAILABLE = True
    log.info("✅  ROS listo. Topic: %s  |  Master: %s", CMD_VEL_TOPIC, ROS_MASTER_URI)

except ImportError as exc:
    log.warning("⚠️  ROS/geometry_msgs no disponible (%s).", exc)
    log.warning("    Ejecutando en MODO SIMULADO: los comandos solo se registran en log.")

except Exception as exc:
    log.warning("⚠️  No se pudo inicializar ROS (%s).", exc)
    log.warning("    Ejecutando en MODO SIMULADO.")


def send_twist(linear_x: float, angular_z: float) -> None:
    """Publica un Twist en ROS o lo simula si ROS no está disponible."""
    log.info("CMD → linear.x=%+.2f  angular.z=%+.2f", linear_x, angular_z)
    if ROS_AVAILABLE and pub is not None:
        pub.publish(_make_twist(linear_x, angular_z))


# ── Mapa de comandos ───────────────────────────────────────────────────────────
# (linear_x, angular_z)
COMMANDS = {
    "forward":        ( LINEAR_SPEED,   0.0          ),
    "backward":       (-LINEAR_SPEED,   0.0          ),
    "forward_left":   ( LINEAR_SPEED,   ANGULAR_SPEED),
    "forward_right":  ( LINEAR_SPEED,  -ANGULAR_SPEED),
    "backward_left":  (-LINEAR_SPEED,  -ANGULAR_SPEED),
    "backward_right": (-LINEAR_SPEED,   ANGULAR_SPEED),
    "stop":           ( 0.0,            0.0          ),
}

# ── Flask app ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)   # Permite peticiones cross-origin desde el kiosco


@app.route("/move", methods=["POST"])
def move():
    """
    Recibe un comando de movimiento.

    Body JSON:  { "command": "forward" }
    Respuesta:  { "status": "ok", "command": "forward", "linear_x": 0.3, "angular_z": 0.0 }
    """
    data    = request.get_json(silent=True) or {}
    command = data.get("command", "").strip().lower()

    if command not in COMMANDS:
        return jsonify({
            "status":  "error",
            "message": f"Comando desconocido. Válidos: {list(COMMANDS)}"
        }), 400

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
    """Detiene el robot de forma segura."""
    send_twist(0.0, 0.0)
    return jsonify({"status": "ok", "command": "stop"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Comprueba que el servidor está activo (usado por la página web)."""
    return jsonify({
        "status":        "ok",
        "ros_available": ROS_AVAILABLE,
        "topic":         CMD_VEL_TOPIC,
        "server_ip":     JETRACER_IP,
        "server_port":   SERVER_PORT,
        "commands":      list(COMMANDS),
    }), 200


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("=" * 60)
    log.info("  JetRacer Web Controller")
    log.info("=" * 60)
    log.info("  Servidor escucha en : http://0.0.0.0:%d", SERVER_PORT)
    log.info("  Accesible desde web : http://%s:%d", JETRACER_IP, SERVER_PORT)
    log.info("  ROS Master URI      : %s", ROS_MASTER_URI)
    log.info("  Topic cmd_vel       : %s", CMD_VEL_TOPIC)
    log.info("  Velocidad lineal    : %.2f m/s", LINEAR_SPEED)
    log.info("  Velocidad angular   : %.2f rad/s", ANGULAR_SPEED)
    log.info("  Modo ROS            : %s", "ACTIVO" if ROS_AVAILABLE else "SIMULADO (sin ROS)")
    log.info("=" * 60)
    log.info("")
    log.info("  ➡️  En la página web pon esta URL:")
    log.info("      http://%s:%d", JETRACER_IP, SERVER_PORT)
    log.info("")

    try:
        # Escucha en 0.0.0.0 para aceptar conexiones desde cualquier interfaz
        # (WiFi, ethernet, localhost). La IP de JETRACER_IP solo se usa para
        # mostrar en log la URL que debes poner en la página web.
        app.run(host="0.0.0.0", port=SERVER_PORT, debug=False, threaded=True)
    except KeyboardInterrupt:
        log.info("🛑  Servidor detenido por el usuario.")
        send_twist(0.0, 0.0)   # seguridad: parar el robot al salir
        sys.exit(0)
