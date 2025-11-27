import sounddevice as sd
import queue
import serial
from vosk import Model, KaldiRecognizer
import json
import os

# ---------------- CONFIG ----------------
SERIAL_PORT = "/dev/ttyACM0"   # <-- CAMBIA AQUÍ si tu puerto es otro
BAUD_RATE = 115200
SAMPLE_RATE = 16000

# Ruta al modelo español dentro del proyecto
MODEL_PATH = os.path.join("my_vosk", "models", "vosk-model-small-es-0.42")
# ----------------------------------------


# -------- ABRIR SERIAL ----------
print(f"Conectando al robot en {SERIAL_PORT} ...")
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print("✔ Robot conectado por USB.\n")


# -------- MODELO VOSK -----------
print("Cargando modelo de voz, espera 3-5 segundos...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("✔ Modelo cargado.\n")


# -------- AUDIO -----------------
audio_q = queue.Queue()

def audio_callback(indata, frames, time, status):
    audio_q.put(bytes(indata))

stream = sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=8000,
    dtype='int16',
    channels=1,
    callback=audio_callback
)
stream.start()

print("🎤 Sistema LISTO. Habla cuando quieras...\n")


# -------- ENVIAR COMANDO -------
def enviar(cmd):
    ser.write((cmd + "\n").encode())
    print(f"→ Enviado al robot: {cmd}")


# -------- TABLA DE COMANDOS -----
# Puedes añadir más cuando quieras
COMANDOS = {
    "adelante": "kwkF",
    "atras": "kwkB",
    "atrás": "kwkB",
    "izquierda": "kwkL",
    "derecha": "kwkR",
    "sentado": "ksit",          # si este os funciona
    "sientate": "ksit",
    "siéntate": "ksit",

    "saluda": "hi",
    "hola": "hi",

    "arriba": "stand",         # ahora lo comentamos
    "levantate": "stand",
    "levántate": "stand",

    "quieto": "balance"
}


# -------- LOOP PRINCIPAL --------
while True:
    data = audio_q.get()

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)['text']

        if text.strip():
            print("📢 Reconocido:", text)

            for palabra, codigo in COMANDOS.items():
                if palabra in text:
                    enviar(codigo)
