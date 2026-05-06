from http import client
import sys
import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "PetoiBLE"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():
    
    comandos = [
        b'ksit\n',
        b'kpee\n',
        b'ksit\n'
        ]

    correctos = [
        b'ksit\n',
        b'kstand\n',
        b'kup\n',
        b'kpee\n',
        b'kck\n',
        b'khi\n',
        b'kwkF\n',
        b'kwkL\n',
        b'ksit\n',
        b'kup\n',
        b'kstand\n'
        ]

    print("Buscando PetoiBLE...")

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
        ## (Opcional) escuchar respuestas
        #def notification_handler(sender, data):
        #    print("RX:", data)

        #await client.start_notify(CHAR_UUID, notification_handler)

        # construimos un conjunto de comandos para probar
        for cmd in comandos:
            await asyncio.sleep(5)
            print("Probando:", cmd)
            # Enviar comando
            await client.write_gatt_char(CHAR_UUID, cmd)
        
        await client.stop_notify(CHAR_UUID)

asyncio.run(main())
