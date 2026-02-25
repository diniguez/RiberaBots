#!/usr/bin/env python3

## previous to this, you should run in another terminal:
## roslaunch jetracer lidar.launch
##

import serial, time, random
import rospy
from sensor_msgs.msg import LaserScan

s = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
obstaculo_detectado = False
DISTANCIA_MINIMA = 0.4

def checksum(data):
    return sum(data) & 0xFF

def velocidad(x_ms, yaw_rads=0.0):
    tmp = bytearray(11)
    tmp[0] = 0xAA; tmp[1] = 0x55
    tmp[2] = 0x0B; tmp[3] = 0x11
    x   = int(x_ms * 1000)
    yaw = int(yaw_rads * 1000)
    tmp[4] = (x   >> 8) & 0xFF; tmp[5] = x   & 0xFF
    tmp[6] = (x   >> 8) & 0xFF; tmp[7] = x   & 0xFF
    tmp[8] = (yaw >> 8) & 0xFF; tmp[9] = yaw & 0xFF
    tmp[10] = checksum(tmp[:10])
    s.write(bytes(tmp)); s.flush()

def lidar_callback(msg):
    global obstaculo_detectado
    n = len(msg.ranges)
    sector = list(msg.ranges[0:n//12]) + list(msg.ranges[11*n//12:])
    validos = [r for r in sector if 0.1 < r < 10.0]
    if validos:
        minimo = min(validos)
        obstaculo_detectado = minimo < DISTANCIA_MINIMA
        if obstaculo_detectado:
            print(f"OBSTACULO DETECTADO a {minimo:.2f} m!")

def evitar():
    print("EVITANDO ...")
    velocidad(-0.2, 0.0)
    time.sleep(1.0)
    sentido = random.choice([-1, 1])
    velocidad(0.0, sentido * 0.6)
    time.sleep(1.5)
    velocidad(0.0)
    time.sleep(0.5)

rospy.init_node('autonomous_node', anonymous=True)
rospy.Subscriber('/scan', LaserScan, lidar_callback)
print("Movimiento autonomo con deteccion de obstaculos iniciado.")
print("Ctrl+C para parar.")

try:
    while not rospy.is_shutdown():
        if obstaculo_detectado:
            velocidad(0.0)
            evitar()
        else:
            x   = random.uniform(0.1, 0.3)
            yaw = random.uniform(-0.4, 0.4)
            dur = random.uniform(1.0, 2.5)
            print(f"EXPLORANDO -> vel={x:.2f} giro={yaw:.2f} tiempo={dur:.1f} s")
            velocidad(x, yaw)
            time.sleep(dur)
            velocidad(0.0)
            time.sleep(0.3)
except KeyboardInterrupt:
    print("Parando robot ...")
    velocidad(0.0)
    s.close()