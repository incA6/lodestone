# base class for device controllers
# code should be able to autonomously control and handle errors for device in a self-contained manner
# provides commands for the device coordinator to use at a user level and notifies the device coordinator of important info
# spawns a separate thread for each device

# relationship to device coordinator:
# - this device controller requires a written notification callback function and a status update callback function from its coordinator
# - this device controller provides available commands to its coordinator
# - this device controller does not require external code to maintain a connection, handle errors, and auto-reboot its device
# - upon encountering an error, this device controller (after handling the error) sends a notification and status update to its coordinator

# coordinator sees: available commands, an auto-updated status, and notifications to be logged

from abc import ABC, abstractmethod
import asyncio

class Device(ABC):

    def __init__(self, device_data : dict, notify_manager):
        self.name = device_data.get("name", "Unknown name.")
        self.desc = device_data.get("desc", "Unknown description.")
        self.type = device_data.get("type", "Unknown device type.")
        self.control_type = device_data.get("control_type", "Unknown control type.")
        self.tech_specs = device_data.get("tech_specs", "Unknown tech specs.")

        self.notify_manager = notify_manager
        self.active = False

    @abstractmethod
    def start(self):
        '''starts autonomous control'''
        pass

    @abstractmethod
    async def status(self):
        '''returns status (on/off) as true/false'''
        pass
