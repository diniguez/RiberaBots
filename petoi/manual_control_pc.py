import queue
import serial
import json
import os
import sys

# ---------------- CONFIG ----------------
SERIAL_PORT = "/dev/ttyACM0"   # <-- CAMBIA AQUÍ si tu puerto es otro
BAUD_RATE = 115200
SAMPLE_RATE = 16000

# -------- ABRIR SERIAL ----------
print(f"Conectando al robot en {SERIAL_PORT} ...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print("✔ Robot conectado por USB.\n")


# -------- ENVIAR COMANDO -------
def enviar(cmd):
    ser.write((cmd + "\n").encode())
    print(f"→ Enviado al robot: {cmd}")


# -------- TABLA DE COMANDOS -----
COMANDOS = {
    "adelante": "kwkF",
    "atras": "kwkB",
    "atrás": "kwkB",
    "izquierda": "kwkL",
    "derecha": "kwkR",
    "sentado": "ksit",
    "sientate": "ksit",
    "siéntate": "ksit",

    # estos aún no funcionan
    "saluda": "hi",
    "hola": "hi",
    "arriba": "stand",
    "levantate": "stand",
    "levántate": "stand",
    "quieto": "balance"
}

# -------- EJECUTAR EL COMANDO INTRODUCIDO EN EL TERMINAL -----
if sys.argv[1]:
    enviar(sys.argv[1])
else:
    enviar("ksit")

ser.close()