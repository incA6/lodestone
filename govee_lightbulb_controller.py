# wrap the code controlling each light into a black box with known functions: on/off, dimmer (if available), warmth (if available), color (if available)
# this inherits from the lightbulb controller class

import datetime

# TODO: temp, add more robust centralized non-hardcoded version later
MAC_ADDRESS = "D4:13:68:C4:45:E3"

# current_time = datetime.now().time()

import asyncio
from govee_ble_local import discover, create_device

async def main():
    devices = await discover(timeout=10, allow_modelled=True)
    info = next(d for d in devices if d.ble_device.address.lower() == MAC_ADDRESS.lower()) # find my govee lightbulb(s)
    bulb = create_device(info.ble_device, info.sku, info.advertisement, allow_modelled=True)

    await bulb.turn_on()
    await bulb.set_brightness(50)
    await bulb.set_rgb((255, 0, 0))
    # await bulb.turn_off()

    await bulb.stop()

# asyncio.run(main())

class GoveeLightbulbController:
    pass

