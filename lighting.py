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

class Lighting:
    '''interfaces with all lights in the setup and allows for user commands + customization'''

    # class variables
    RETRY_TIMER = 60 # seconds

    def __init__(self, settings_file_loc):
        self.disconnected_lights = []
        self.settings_file_loc = settings_file_loc

    def run(self):
        pass

    async def retry(self):
        for light in self.disconnected_lights:
            print(f"Retrying a connection to {light.name}.")
            try:
                if (light.connect()):
                    # light connected successfully, add to mark as active and remove from list
                    # TODO: mark as active
                    self.disconnected_lights.remove(light)
            except:
                #TODO: log error to console
                pass
        
        await asyncio.sleep(Lighting.RETRY_TIMER) # we let the cpu go back to whatever it's doing before coming here again in 60 seconds
                
            
set1 = Lighting()