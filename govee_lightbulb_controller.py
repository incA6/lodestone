# fully-auto controller for Govee smart bluetooth lightbulbs, controlled via bluetooth and MAC address

import asyncio
from govee_ble_local import discover, create_device

from device import Device

class GoveeLightbulbController(Device):

    COMMAND_LIST = ["change setting []"]
    AVAILABLE_SETTINGS = ["on_off", "brightness"]

    def __init__(self, device_data : dict, notify_manager):
        super().__init__(device_data, notify_manager)
        self.MAC = self.tech_specs.get("MAC_address", "unknown")

        self.stay_connected = True

        # validate input data before starting
        if self.tech_specs.get("bulb_type") != "Govee" or self.MAC == "unknown":
            self.active = False
            self.notify_manager("Error: invalid device setup")
        else:
            self.active = True

    def start(self):
        '''starts autonomously staying connected to and managing lightbulb'''
        asyncio.run(self.connect())

    async def status(self):
        '''returns status (on/off)'''
        return self.active

    async def connect(self):
        '''connect to the lightbulb if necessary, throws error if fail'''

        self.notify_manager("Log: connecting Govee lightbulb")
        
        devices = await discover(timeout=10, allow_modelled=True)
        info = next((d for d in devices if d.ble_device.address.lower() == self.MAC.lower()), None)
        if info is None:
            self.active = False
            self.notify_manager("Error: connection failed")
            return
        self.bulb = create_device(info.ble_device, info.sku, info.advertisement, allow_modelled=True)

        self.notify_manager("Log: successfully connected")
        self.active = True

        await self.start_heartbeat()

    async def start_heartbeat(self):
        '''periodically pings the lightbulb to maintain a connection'''
        
        while self.stay_connected:
            connection_status = await self.test_connection()
            if connection_status != True:
                self.notify_manager(f"Error: device disconnected ({connection_status})")
                await self.connect() # retry connection
            await asyncio.sleep(8)


    async def turn_on(self):
        try:
            await asyncio.wait_for(self.bulb.turn_on(), timeout=5.0)
        except Exception as e:
            self.notify_manager(f"Error: command failed ({e})")
    

    async def turn_off(self):
        try:
            await asyncio.wait_for(self.bulb.turn_off(), timeout=5.0)
        except Exception as e:
            self.notify_manager(f"Error: command failed ({e})")

    async def set_brightness(self, brightness: int):
        '''brightness from 0-100, if available. returns False if unavailable'''
        pass

    async def set_rgb(self, r: int, g: int, b: int):
        '''rgb, if available. returns False if unavailable'''
        pass

    async def test_connection(self):
        '''returns True if connected, Error message if disconnected'''
        try:
            await self.bulb.update()
            return True
        except Exception as e:
            return e

    async def repeated_flahes(self, on_off: bool):
        '''flashes repeatedly, if available (not safe for power switches)'''
        pass    





# TESTING

def print_notif(notif):
    print(f"Notification: {notif}")

if __name__ == "__main__":
    data = {
        "name": "light_1",
        "desc": "main light",
        "type": "light",
        "control_type": "bluetooth",
        "tech_specs": {
                "bulb_type": "Govee",
                "brightness": 1600,
                "controllable_brightness": True,
                "controllable_color": True,
                "controllable_warmth": True,
                "MAC_address": "D4:13:68:CB:39:8D"
        }
    }

    L1 = GoveeLightbulbController(data, print_notif)
    L1.start()

    while True:
        print("Commands: q, on, off")
        answer = input()
        if answer.lower() == "q":
            print("exiting")
            break

        elif answer.lower() == "on":
            if (L1.active):
                L1.turn_on
            else:
                print("light not active")

        elif answer.lower() == "off":
            if (L1.active):
                L1.turn_off
            else:
                print("light not active")
        
        else:
            print("not a command")