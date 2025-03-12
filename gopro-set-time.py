import os

# Set locale only for this script
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"

import asyncio
import time
from datetime import datetime, timezone
from open_gopro import WirelessGoPro, constants

GOPRO_MAC = "CF:FC:D6:26:D4:EB"

async def setup_gopro():
    gopro = WirelessGoPro(ble_mac=GOPRO_MAC)
    
    print("Checking BLE connection...")
    
    if not gopro.is_ble_connected:
        print("GoPro is not connected via BLE. Trying to connect...")
        await gopro.open()

    print(f"BLE Connected: {gopro.is_ble_connected}")

    # try:
    #     cam_status = await gopro.ble_command.get_camera_statuses()
    #     print(cam_status)
    # except Exception as e:
    #     print(f"❌ Failed to get camera status: {e}")

    try:
         # 🔴 Start Recording
        print("🎥 Starting Recording...")
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.ENABLE)
        print("✅ Recording Started!")

        # Record for 10 seconds
        await asyncio.sleep(10)

        # 🛑 Stop Recording
        print("🛑 Stopping Recording...")
        await gopro.ble_command.set_shutter(shutter=constants.Toggle.DISABLE)
        print("✅ Recording Stopped!")
    except Exception as e:
        print(f"❌ Failed to set shutter: {e}")

    # try:
    #     current_time = datetime.now()
    #     await gopro.ble_command.set_date_time(date_time=current_time)
    #     print("✅ Date & Time updated successfully!")
    # except Exception as e:
    #     print(f"❌ Failed to set time: {e}")

    # try:
    #     await gopro.ble_command.enable_wifi_ap(enable=True)
    #     print("✅ AP enabled successfully!")
    # except Exception as e:
    #     print(f"❌ Failed to enable AP: {e}")

    # try:
    #     stream_url = "rtmp://192.168.1.29"
    #     await gopro.ble_command.set_livestream_mode(
    #         url=stream_url,
    #         minimum_bitrate=800,   # Minimum bitrate (800 kbps)
    #         maximum_bitrate=4000,  # Maximum bitrate (Adjust as needed)
    #         starting_bitrate=2000  # Start at 2000 kbps (within 800-8000 range)
    #     )
    #     print("✅ Livestream set successfully!")
    #     await asyncio.sleep(60)
    # except Exception as e:
    #     print(f"❌ Failed to set livestream: {e}")

    await gopro.close()
    print("Disconnected from GoPro.")

asyncio.run(setup_gopro())

