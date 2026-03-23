import asyncio
from bleak import BleakClient

ADDRESS = "54:37:45:9A:9A:E1"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Conectado 🐾")

        services = client.services

        for service in services:
            print(f"[Servicio] {service.uuid}")
            for char in service.characteristics:
                print(f"  └─ {char.uuid} | {char.properties}")

asyncio.run(main())