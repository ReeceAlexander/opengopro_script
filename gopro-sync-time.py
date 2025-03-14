import os

# Set locale only for this script
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

import asyncio
from datetime import datetime
from open_gopro import WirelessGoPro, constants

GOPRO_MAC = "CF:FC:D6:26:D4:EB"

async def sync_gopro_time():
    gopro = WirelessGoPro(ble_mac=GOPRO_MAC)
    
    print("Checking BLE connection...")
    
    if not gopro.is_ble_connected:
        print("GoPro is not connected via BLE. Trying to connect...")
        await gopro.open()

    print(f"BLE Connected: {gopro.is_ble_connected}")

    try:
        current_time = datetime.now()
        await gopro.ble_command.set_date_time(date_time=current_time)
        print("Date & Time updated successfully!")
    except Exception as e:
        print(f"Failed to set time: {e}")

    await gopro.close()
    print("Disconnected from GoPro.")

asyncio.run(sync_gopro_time())

