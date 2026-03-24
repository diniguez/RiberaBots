import sys
import asyncio
from bleak import BleakScanner, BleakClient

ADDRESS = "54:37:45:9A:9A:E1"
CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():
    async with BleakClient(ADDRESS) as client:
        await client.write_gatt_char(CHAR_UUID, bytes([0x6B, 0x73, 0x69, 0x74]))

asyncio.run(main())