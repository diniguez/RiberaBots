from djitellopy import Tello

def conectar_tello():
    tello = Tello()
    tello.connect()
    return tello

def obtener_bateria(tello):
    return tello.get_battery()

tello = conectar_tello()
bateria = obtener_bateria(tello)
print(f"Nivel de batería: {bateria}%")
    
