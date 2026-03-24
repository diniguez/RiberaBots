'''
    This works only for Bluetooth standard, not for BLE (Bluetooht Low Energy)
'''

import serial
import sys
import time

# -------- CONFIG ----------------
SERIAL_PORT = "/dev/rfcomm0"   # <-- CAMBIA AQUÍ si tu puerto es otro
BAUD_RATE = 115200
SAMPLE_RATE = 16000

# -------- ABRIR SERIAL ----------
print(f"Conectando al robot en {SERIAL_PORT} ...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
ser.flush()
print("✔ Robot conectado por Bluetooth.\n")


# -------- ENVIAR COMANDO -------
def enviar(cmd):
    ser.write((cmd + "\n").encode())
    print(f"→ Enviado al robot: {cmd}")
    respuesta = ser.readline().decode().strip()
    print("🐾 Respuesta del robot:", respuesta)

    if ser.in_waiting > 0:
        respuesta = ser.readline().decode().strip()
        data = ser.readline().decode(errors="ignore").strip()
        print("🐾 Respuesta del robot:", respuesta, data)
    
    ser.flush()

# -------- EJECUTAR EL COMANDO INTRODUCIDO EN EL TERMINAL -----
if len(sys.argv) > 1:
    enviar(sys.argv[1])
else:
    print(f"→ Enviado al robot un movimiento por defecto")
    enviar("ksit")

time.sleep(1)
ser.close()


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
