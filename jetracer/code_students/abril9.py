import serial, time, random
import rospy
from sensor_msgs.msg import LaserScan

# ---------- SERIAL ----------
s = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# ---------- VARIABLES ----------
obstaculo_detectado = False
DISTANCIA_MINIMA = 0.5

# ---------- CONTROL DEL ROBOT ----------

def checksum(data):
    return sum(data) & 0xFF

def velocidad(x_ms, yaw_rads=0.0):
    tmp = bytearray(11)
    tmp[0] = 0xAA; tmp[1] = 0x55
    tmp[2] = 0x0B; tmp[3] = 0x11

    x   = int(x_ms * 1000)
    yaw = int(yaw_rads * 1000)

    tmp[4] = (x >> 8) & 0xFF; tmp[5] = x & 0xFF
    tmp[6] = (x >> 8) & 0xFF; tmp[7] = x & 0xFF
    tmp[8] = (yaw >> 8) & 0xFF; tmp[9] = yaw & 0xFF
    tmp[10] = checksum(tmp[:10])

    s.write(bytes(tmp))
    s.flush()

# ---------- LIDAR ----------

def lidar_callback(msg):
    global obstaculo_detectado
    n = len(msg.ranges)

    # Sector frontal.
    sector = list(msg.ranges[0:n//12]) + list(msg.ranges[11*n//12:])
    validos = [r for r in sector if 0.1 < r < 10.0]

    if validos:
        obstaculo_detectado = min(validos) < DISTANCIA_MINIMA

# ---------- MOVIMIENTO DE INICIO ----------

def movimiento_inicio():
    
    vel = 0.45  # velocidad constante 

    velocidad(vel)
    time.sleep(2)

    giro = -0.3   # giro constante
    vel = 0.25  # velocidad constante 

    velocidad(vel, giro)
    time.sleep(2)


# ---------- EVITAR OBSTÁCULO ----------

def evitar_obstaculo():
    print("Obstáculo detectado")

    velocidad(vel)
    time.sleep(2)

    giro2 = 0.3   # giro constante
    vel = -0.25  # velocidad constante 

    velocidad(vel, giro2)
    time.sleep(1,1.5)


# ---------- PROGRAMA PRINCIPAL ----------

rospy.init_node('jetracer_random', anonymous=True)
rospy.Subscriber('/scan', LaserScan, lidar_callback)

inicio = time.time()
DURACION = 90  # segundos mínimo

try:
    movimiento_inicio()
    while not rospy.is_shutdown() and time.time() - inicio < DURACION:

        if obstaculo_detectado:
            evitar_obstaculo()
    # Parar al final
    velocidad(0.0)

except KeyboardInterrupt:
    velocidad(0.0)
    s.close()
