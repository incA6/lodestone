# wrap the code controlling each light into a black box with known functions: on/off, dimmer (if available), warmth (if available), color (if available)
# this inherits from the lightbulb controller class
# design: does the thing and throws and error if it doesn't work

# TODO: temp, add more robust centralized non-hardcoded version later
# MAC_ADDRESS = "D4:13:68:C4:45:E3"

# current_time = datetime.now().time()

import asyncio
from govee_ble_local import discover, create_device

from lightbulb_controller import LightbulbController

class GoveeLightbulbController(LightbulbController):
    def __init__(self, name, MAC_ADDRESS, check_status_callback=None):
        super().__init__(name)
        self.MAC = MAC_ADDRESS
        self.bulb = None
        self.check_status_callback = check_status_callback # call back function to let the lighting interface know to check its lights

    async def connect(self):
        '''connect to the lightbulb if necessary, throws error if fail'''
        
        devices = await discover(timeout=10, allow_modelled=True)
        info = next((d for d in devices if d.ble_device.address.lower() == self.MAC.lower()), None)

        if info is None:
            raise BulbNotFound(f"Bulb not found: {self.MAC}")

        self.bulb = create_device(info.ble_device, info.sku, info.advertisement, allow_modelled=True)

    async def disconnect(self):
        '''disconnect from the lightbulb if available'''
        pass

    async def turn_on(self):
        try:
            await asyncio.wait_for(self.bulb.turn_on(), timeout=5.0)
        except Exception as e:
            await self.check_status_callback()
    

    async def turn_off(self):
        try:
            await asyncio.wait_for(self.bulb.turn_off(), timeout=5.0)
        except Exception as e:
            await self.check_status_callback()

    async def set_brightness(self, brightness: int):
        '''brightness from 0-100, if available. returns False if unavailable'''
        pass

    async def set_rgb(self, r: int, g: int, b: int):
        '''rgb, if available. returns False if unavailable'''
        pass

    async def test_connection(self):
        '''throws error if disconnected'''
        try:
            await self.bulb.update()
        except Exception as e:
            raise BulbNotConnected(e)

    async def status(self):
        '''returns status (on/off)'''
        pass

    async def repeated_flahes(self, on_off: bool):
        '''flashes repeatedly, if available (not safe for power switches)'''
        pass    

class BulbNotFound(Exception):
    pass

class BulbNotConnected(Exception):
    pass





# TESTING


async def test():

    L1 = None # light

    # user input loop
    while True:
        print("Commands: q, connect, on, off, flash")
        answer = input()
        if answer.lower() == "q":
            print("exiting")
            break
        elif answer.lower() == "connect": # what happens if we connect after already connected?
            L1 = GoveeLightbulbController("L1", "D4:13:68:C4:45:E3")

            print(f"Searching for bulb: {L1.name}")
            try:
                print("Connecting...")
                await L1.connect()
                print("Testing connection...")
                await L1.test_connection()
                L1.active = True
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
                L1.active = False
                continue

            print("Connection successful!")

        elif answer.lower() == "on":
            if (L1.active):
                try:
                    await L1.turn_on()
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
            else:
                print("light not active")

        elif answer.lower() == "off":
            if (L1.active):
                try:
                    await L1.turn_off()
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
            else:
                print("light not active")

        elif answer.lower() == "flash":
            if (L1.active):
                try:
                    for i in range(5):
                        await L1.turn_on()
                        await asyncio.sleep(0.5)
                        await L1.turn_off()
                        await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"{type(e).__name__}: {e}")
            else:
                print("light not active")
            

        else:
            print("not a command")



if __name__ == "__main__":
    asyncio.run(test())