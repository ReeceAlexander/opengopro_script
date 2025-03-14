import os

# Set locale only for this script
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

import asyncio
from open_gopro import WirelessGoPro, constants

GOPRO_MAC = "CF:FC:D6:26:D4:EB"

async def stop_gopro_rec():
    gopro = WirelessGoPro(ble_mac=GOPRO_MAC)
    
    print("Checking BLE connection...")
    
    if not gopro.is_ble_connected:
        print("GoPro is not connected via BLE. Trying to connect...")
        await gopro.open()

    print(f"BLE Connected: {gopro.is_ble_connected}")

    try:
        print("Stopping Recording...")
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.DISABLE)
        print("Recording Stopped!")

    except Exception as e:
        print(f"Failed to set shutter: {e}")

    await gopro.close()
    print("Disconnected from GoPro.")

asyncio.run(stop_gopro_rec())

