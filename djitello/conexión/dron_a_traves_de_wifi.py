from djitellopy import Tello
import time

# Datos de tu red Wi-Fi
SSID = 'RiberaBots-1_IoT'
PASSWORD = 'campeonato'

# Crear instancia del dron
tello = Tello()

# Conectar al dron (asegúrate de estar conectado al red wifi propia del dron)
tello.connect()

# Activar SDK (esto lo hace .connect() automáticamente, pero por seguridad lo repetimos)
tello.send_control_command("command")

# Enviar comando para configurar modo Router
cmd = f"ap {SSID} {PASSWORD}"
print(f"Enviando: {cmd}")
tello.send_control_command(cmd)

# Cerrar conexión
tello.end()

print("\n✅ Listo. Cambia el interruptor del dron a Router Mode y reinícialo.")