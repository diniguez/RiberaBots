from djitellopy import Tello
import time

tello = Tello()
tello.connect()

bateria = tello.get_battery()
print(f"Nivel de batería: {bateria}%")

tello.takeoff()
time.sleep(2)

tello.flip_forward()
time.sleep(2)

tello.flip_back()
time.sleep(2)

tello.land()
