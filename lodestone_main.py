# main central loop to control user input, lighting mode, sending pings, saving data, etc.

import threading
import asyncio

from lighting_interface import *

# server management thread

# lighting and sensor control thread
def lighting_manager(lighting_interface):
    lighting_interface.start()


# user input thread
def console_controller(lighting_interface):

    print("=========================================================")
    print("\t\tWelcome to the Lodestone.")
    print("=========================================================")
    print()

    HELP = '''Commands List:
                1 - ON
                2 - OFF
                3'''

    # user input loop
    while True:
        print("Please enter a command. Q for quit. Help for a commands list.")
        answer = input()
        if answer.lower() == "q":
            print("Exiting console.")
            break

        elif answer.lower() == "1":
            print("queueing ON command")
            lighting_interface.queue_command("light1", "on")

        elif answer.lower() == "2":
            print("queueing OFF command")
            lighting_interface.queue_command("light1", "off")

        elif answer.lower() == "help": 
            print(HELP)

        else:
            print("Unknown command.")

# main thread
def main():
    threads = []
    lighting_interface = LightingInterface("f")

    threads.append( threading.Thread(target=console_controller, args=(lighting_interface,)) ) # console
    threads.append( threading.Thread(target=lighting_manager, args=(lighting_interface,)) ) # lighting

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("Program complete.")

if __name__ == "__main__":
    main()
