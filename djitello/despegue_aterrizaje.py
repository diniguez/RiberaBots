from djitellopy import Tello

tello = Tello()
tello.connect()

bateria = tello.get_battery()
print(f"Nivel de batería: {bateria}%")

tello.takeoff()
tello.land()
