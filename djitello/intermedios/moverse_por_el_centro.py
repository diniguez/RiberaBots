from djitellopy import Tello
import time

tello = Tello()
tello.connect()

bateria = tello.get_battery()
print(f"Nivel de batería: {bateria}%")

# despegar y tomar altura de seguridad (2 metros)
tello.takeoff()
time.sleep(2)

tello.move_up(150)
time.sleep(2)
altura = tello.get_height()
print(f"Altura: {altura}%")

# salir del edificio F
tello.move_forward(50)
time.sleep(2)

tello.move_left(250)
time.sleep(5)

tello.move_forward(400)
time.sleep(8)

# moverse por la rampa
tello.move_right(800)
time.sleep(16)

# acercarse al edificio B
tello.move_forward(1600)
time.sleep(32)

# ponerse a la altura de las ventanas de la planta 0
tello.move_up(100)
time.sleep(2)
altura = tello.get_height()
print(f"Altura planta 0: {altura}%")

# recorrer las ventanas
tello.move_left(1600)
time.sleep(32)

# ponerse a la altura de las ventanas de la planta 1
tello.move_up(300)
time.sleep(12)
altura = tello.get_height()
print(f"Altura planta 1: {altura}%")

# recorrer las ventanas
tello.move_right(1600)
time.sleep(32)

# ponerse a la altura de las ventanas de la planta 2
tello.move_up(300)
time.sleep(12)
altura = tello.get_height()
print(f"Altura planta 2: {altura}%")

# recorrer las ventanas
tello.move_left(1600)
time.sleep(32)

# recorrer las ventanas
tello.move_right(1600)
time.sleep(32)

# descender a altura de seguridad (2 metros)
tello.move_down(700)
time.sleep(12)
altura = tello.get_height()
print(f"Altura: {altura}%")

# volver del edificio B al F
tello.rotate_clockwise(180)
time.sleep(4)
tello.move_forward(1600)
time.sleep(32)

# moverse por la rampa
tello.move_right(800)
time.sleep(16)

# entrar del edificio F
tello.move_forward(400)
time.sleep(8)

tello.move_forward(50)
time.sleep(2)

tello.move_left(250)
time.sleep(5)

# girar y aterrizar en el punto de partida
tello.rotate_clockwise(180)
time.sleep(4)
tello.land()