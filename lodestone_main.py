# main central loop to control user input, lighting mode, sending pings, saving data, etc.

import threading
import asyncio

from lighting import Lighting

# server management thread

# lighting and sensor control thread

# user input thread
def console_input_loop():

    print("=========================================================")
    print("\t\tWelcome to the Lodestone.")
    print("=========================================================")
    print()

    HELP = '''Commands List:
                1
                2 
                3'''

    # user input loop
    while True:
        print("Please enter a command. Q for quit. Help for a commands list.")
        answer = input()
        if answer.lower() == "q":
            print("Exiting console.")
            break

        elif answer.lower() == "help": 
            print(HELP)

        else:
            print("Unknown command.")

# main thread
def main():
    threads = []

    threads.append( threading.Thread(target=console_input_loop) )

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("Program complete.")

if __name__ == "__main__":
    main()
