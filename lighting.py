# upon run/initialization:
# attempts to set up lights according to lighting data file (contains lights, configurations, schedules)
    # if lighting connection fails, logs to console and skip (lightbulb setups must throw error upon failure)
# marks all successful lights in an array (0 for unavailable, 1 for working) for the configurations
# turns on current configuration according to schedule (if on), otherwise goes to default
    # if a light is not available // does not respond correctly, this code skips it and adds the light to the retry list
# background process periodically retries the lights

# interface with this class:
# 1. press play to auto run on schedule
# 2. manual override via user commands (this class provides command list by giving access to all lights)
# 3. set up new configurations w/ available lights currently loaded AND save to file
# 4. add/remove lights to file (updates old configurations)
# 5. (very optional) run diagnostic by turning on and off each light to test

import asyncio

from govee_lightbulb_controller import *

class Lighting:
    '''interfaces with all lights in the setup and allows for user commands + customization'''

    # class variables
    RETRY_TIMER = 60 # seconds

    def __init__(self, settings_file_loc):
        self.settings_file_loc = settings_file_loc
        self.lighting_matrix = []
        self.disconnected_lights = []

        self.read_lighting_file(self.settings_file_loc)

    def start(self):
        asyncio.start(self.main())

    # main async entry point
    async def main(self):
        # attempt to connect to each registered light
        for light in self.lighting_matrix:
            try:
                await light.connect()
                await light.test_connection()
            except Exception as e:
                # light failed to connect, add to disconnected list
                print(f"{type(e).__name__}: {e}")
                light.active = False
                if light not in self.disconnected_lights:
                    self.disconnected_lights.append(light)
                continue

            # light works, mark as active
            print(f"Light: {light.name} is connected.")
            light.active = True


    def read_lighting_file(self, settings_file_loc):
        '''reads expected lights, configurations, schedules from file ---> then initializes lights (ie. lighting matrix)'''
        # must be run again if configurations or lights change
        
        # TODO: (fix) temp, for now, add just the one govee lightbulb to the matrix
        light1 = GoveeLightbulbController("light1", "D4:13:68:C4:45:E3")
        self.lighting_matrix.append(light1)

    async def retry(self):
        '''periodically retries all disconnected lights'''

        for light in self.disconnected_lights:
            print(f"Retrying a connection to {light.name}.")
            try:
                await light.connect()
                await light.test_connection()
            except:
                #TODO: log error to console
                continue # skip

            # light connected successfully, add to mark as active and remove from list
            light.active = True
            self.disconnected_lights.remove(light)
        
        await asyncio.sleep(Lighting.RETRY_TIMER) # we let the cpu go back to whatever it's doing before coming here again in 60 seconds