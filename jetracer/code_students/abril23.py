import serial, time, random
import rospy
import random
from sensor_msgs.msg import LaserScan

s = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

obstaculo_detectado = True
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

    sector = list(msg.ranges[0:n//4]) + list(msg.ranges[11*n//4:])
    validos = [r for r in sector if 0.1 < r < 40.0]

    if validos:
        obstaculo_detectado = min(validos) < DISTANCIA_MINIMA

# ---------- EVITAR OBSTÁCULO SIMPLE ----------

def empujar():
    velocidad(0.0)
    time.sleep(0.3)

    velocidad(0.70, 0.0)   # avanza
    time.sleep(1.0)

def buscar():

    velocidad(0.0)
    time.sleep(0.1)

    velocidad(velocidad2, mov)
    time.sleep(2)

# ---------- PROGRAMA PRINCIPAL ----------
rospy.init_node('reto1_jetracer', anonymous=True)
rospy.Subscriber('/scan', LaserScan, lidar_callback)

inicio = time.time()
DURACION = 90   # segundos



try:
    while not rospy.is_shutdown() and time.time() - inicio < DURACION:

        if obstaculo_detectado:
            empujar()
        else:
            buscar()

except KeyboardInterrupt:
    velocidad(0.0)
    s.close()
