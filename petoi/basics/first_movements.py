from http import client
import sys
import asyncio
from bleak import BleakScanner, BleakClient

#ADDRESS = "54:37:45:9A:9A:E1"
ADDRESS = "31:02:00:01:36:3D" 
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():
    
    comandos = [
        b'kup\n',
        b'kbflip\n'        
        ]

    comandos_validados = [
        b'kpee\n',
        b'kck\n',
        b'khi\n',
        b'kvtF\n',
        b'kwkF\n',
        b'kwkL\n',
        b'ksit\n',
        b'kup\n',
        b'kstand\n'
        ]

    comandos_no_validos = [
        b'kflip\n'
        ]

    print(f"Conectando a {ADDRESS}...")

    async with BleakClient(ADDRESS) as client:
        print("Conectado 🐾")
        ## (Opcional) escuchar respuestas
        #def notification_handler(sender, data):
        #    print("RX:", data)

        #await client.start_notify(CHAR_UUID, notification_handler)

        # construimos un conjunto de comandos para probar
        for cmd in comandos:
            await asyncio.sleep(2)
            print("Probando:", cmd)
            # Enviar comando
            await client.write_gatt_char(CHAR_UUID, cmd)
        
        await client.stop_notify(CHAR_UUID)

asyncio.run(main())
