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
import threading

import time # testing

from govee_lightbulb_controller import *

class LightingInterface:
    '''interfaces with all lights in the setup and allows for user commands + customization'''

    # class variables
    RETRY_TIMER = 30 # seconds
    CONNECTION_TEST_TIMER = 10 # seconds
    
    VALID_COMMANDS = ["on", "off"]

    def __init__(self, settings_file_loc):
        self.settings_file_loc = settings_file_loc
        self.lighting_matrix = []
        self.disconnected_lights = []
        self.command_queue = asyncio.Queue() # <--- this is not thread safe so we use self.loop below

        # to keep queue thread safe
        self.loop = None # this will be the current running event loop
        self.loop_ready = threading.Event()

    def start(self):
        self.read_lighting_file(self.settings_file_loc)
        asyncio.run(self.main())

    def get_available_lights(self):
        return [light for light in self.lighting_matrix if light.active == True]

    def queue_command(self, target, command, args=None):
        '''public method to call a command'''
        # target = light name

        # find target light
        light = None
        for l in self.lighting_matrix:
            if l.name == target:
                light = l
                break
        if light == None: # target light not found
            raise LightNotFound(f"Light: {target} not found")
        
        # check valid command
        if command not in self.VALID_COMMANDS:
            raise InvalidLightingCommand(f"{command} not in {self.VALID_COMMANDS}")
        
        # append command to queue (in a threadsafe manner)
        self.loop_ready.wait()
        self.loop.call_soon_threadsafe(self.command_queue.put_nowait,(light, command, args))
        
        


    # main async entry point
    async def main(self):
        self.loop = asyncio.get_running_loop() # get a reference to current running loop
        self.loop_ready.set() # now, after the reference is set, we signal that the loop is ready for command queue

        # attempt to connect to each registered light
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self.connect_light(light)) for light in self.lighting_matrix]
        # ^^ waits for all of these to be done before going forward

        # start retry loop
        asyncio.create_task(self.retry())

        # start auto connection test loop
        asyncio.create_task(self.connection_test_loop())

        # start command processing loop that waits for new tasks and then STARTS them whenever they come in (since we have to wait for most of them)
        while True:
            light, command, args = await self.command_queue.get()

            # process command
            try:
                if command == LightingInterface.VALID_COMMANDS[0]: # on
                    asyncio.create_task(light.turn_on())
                elif command == LightingInterface.VALID_COMMANDS[1]: # off
                    asyncio.create_task(light.turn_off())
            except Exception as e:
                print(f"Command failed: {e}")
                


    async def connect_light(self, light):
        print(f"Attempting to connect: {light.name}")
        try:
            await light.connect()
            await light.test_connection()

            # light works, mark as active
            print(f"Light: {light.name} is connected.")
            light.active = True
            if light in self.disconnected_lights:
                self.disconnected_lights.remove(light)
        except Exception as e:
            # light failed to connect, add to disconnected list
            print(f"{type(e).__name__}: {e}")
            light.active = False
            if light not in self.disconnected_lights:
                self.disconnected_lights.append(light)

    def read_lighting_file(self, settings_file_loc):
        '''reads expected lights, configurations, schedules from file ---> then initializes lights (ie. lighting matrix)'''
        # must be run again if configurations or lights change
        
        # TODO: (fix) temp, for now, add just the one govee lightbulb to the matrix
        light1 = GoveeLightbulbController("light1", "D4:13:68:C4:45:E3")
        self.lighting_matrix.append(light1)

    async def retry(self):
        '''periodically retries all disconnected lights'''

        while True:
            # print("retry loop")
            for light in self.disconnected_lights:
                await self.connect_light(light)
            
            await asyncio.sleep(LightingInterface.RETRY_TIMER) # we let the cpu go back to whatever it's doing before coming here again in 60 seconds

    async def connection_test_loop(self):
        '''periodically checks all active lights (if the lights are checkable)'''
        while True:
            # print("connection test loop")
            for light in self.lighting_matrix:
                if (light.active):
                    try:
                        await light.test_connection()
                    except Exception as e:
                        # light disconnected
                        print(f"{light.name} found disconnected.")
                        light.active = False
                        if light not in self.disconnected_lights:
                            self.disconnected_lights.append(light)
            
            await asyncio.sleep(LightingInterface.CONNECTION_TEST_TIMER) # we let the cpu go back to whatever it's doing before coming here again in 60 seconds


class LightNotFound(Exception):
    pass

class InvalidLightingCommand(Exception):
    pass



# TESTING

def console(lighting):

    print("=========================================================")
    print("\t\tWelcome to the Lodestone.")
    print("=========================================================")
    print()

    HELP = '''Commands List:
                1 -- on
                2 -- off
                '''

    # user input loop
    while True:
        print("Please enter a command. Q for quit. Help for a commands list.")
        answer = input()
        if answer.lower() == "q":
            print("Exiting console.")
            break

        elif answer.lower() == "1":
            print("queueing ON command")
            lighting.queue_command("light1", "on")

        elif answer.lower() == "2":
            print("queueing OFF command")
            lighting.queue_command("light1", "off")

        elif answer.lower() == "help": 
            print(HELP)

        else:
            print("Unknown command.")

def main():
    lighting = LightingInterface("current_device_list.txt")

    t1 = threading.Thread(target=console, args=(lighting,))
    t2 = threading.Thread(target=lighting.start)
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    

if __name__ == "__main__":
    main()