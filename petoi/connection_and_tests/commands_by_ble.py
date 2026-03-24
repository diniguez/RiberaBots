import sys
import asyncio
from bleak import BleakScanner, BleakClient

ADDRESS = "54:37:45:9A:9A:E1"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():
    if len(sys.argv) < 2:
        print("Uso: python3 bittle_ble.py <comando>")
        return

    comando = sys.argv[1]

    print(f"Conectando a {ADDRESS}...")

    async with BleakClient(ADDRESS) as client:
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