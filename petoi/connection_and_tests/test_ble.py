import sys
import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "PetoiBLE"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():
    if len(sys.argv) < 2:
        print("Uso: python3 bittle_ble.py <comando>")
        return

    comando = sys.argv[1]

    print("Buscando Bittle...")

    devices = await BleakScanner.discover()
    target = None

    for d in devices:
        print(f"Encontrado: {d.name} [{d.address}]")
        if d.name and DEVICE_NAME in d.name:
            target = d
            break

    if not target:
        print("No se encontró Bittle 😢")
        return

    print(f"Conectando a {target.address}...")

    async with BleakClient(target.address) as client:
        print("Conectado 🐾")

        # (Opcional) escuchar respuestas
        def notification_handler(sender, data):
            print("RX:", data)

        await client.start_notify(CHAR_UUID, notification_handler)

        # Enviar comando
        await client.write_gatt_char(CHAR_UUID, (comando + "\n").encode())

        print(f"Enviado: {comando}")

        await asyncio.sleep(2)

        await client.stop_notify(CHAR_UUID)

asyncio.run(main())