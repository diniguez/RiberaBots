from djitellopy import Tello
import time

tello = Tello()
tello.connect()

bateria = tello.get_battery()
print(f"Nivel de batería: {bateria}%")

tello.takeoff()

tello.flip_forward()

tello.land()
