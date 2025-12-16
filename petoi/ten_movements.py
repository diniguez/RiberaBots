import serial
import sys
import time

# -------- CONFIG ----------------
SERIAL_PORT = "/dev/ttyACM0"   # <-- CAMBIA AQUÍ si tu puerto es otro
BAUD_RATE = 115200
SAMPLE_RATE = 16000

# -------- ABRIR SERIAL ----------
print(f"Conectando al robot en {SERIAL_PORT} ...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("✔ Robot conectado por USB.\n")


# -------- ENVIAR COMANDO -------
def enviar(cmd):
    ser.write((cmd + "\n").encode())
    print(f"→ Enviado al robot: {cmd} \n")
    time.sleep(5)


# -------- CONJUNTO DE DIEZ MOVIMIENTOS POR DEFECTO -------
def diez_movimientos():
    for indice in range(10):
        print(f"paso {indice}")
        enviar("khsk")

# -------- EJECUTAR UN MOVIMIENTO POR DEFECTO -----
enviar("kup")

# -------- EJECUTAR MOVIMIENTOS PROGRAMADOS -----
diez_movimientos()

# -------- CERRAR COMUNICACION CON ROBOT -----
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
