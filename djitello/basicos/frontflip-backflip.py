from djitellopy import Tello
import time

tello = Tello()
tello.connect()

bateria = tello.get_battery()
print(f"Nivel de batería: {bateria}%")

tello.takeoff()
time.sleep(2)

tello.move_forward(200)

tello.move_up(100)

tello.flip_forward()
time.sleep(2)
tello.move_up(100)
tello.move_down(100)

tello.flip_back()

tello.rotate_clockwise(360)
time.sleep(2)

tello.land()
