from djitellopy import Tello

def conectar_tello():
    """
    Conecta al dron Tello y devuelve la instancia del objeto Tello.
    
    Returns:
        Tello: Instancia conectada del dron Tello.
    """
    tello = Tello()
    tello.connect()
    return tello
def obtener_bateria(tello):
    """
    Obtiene el nivel de batería del dron Tello.

    Args:
        tello (Tello): Instancia del dron Tello.

    Returns:
        int: Nivel de batería en porcentaje.
    """
    return tello.get_battery()
# Ejemplo de uso
if __name__ == "__main__":
    tello = conectar_tello()
    bateria = obtener_bateria(tello)
    print(f"Nivel de batería: {bateria}%")
    
