# base class for device controllers
# code should be able to fully control and handle errors for device in a self-contained manner

# relationship to device coordinator:
# - this device controller requires a written notification callback function and a status update callback function from its coordinator
# - this device controller provides available commands to its coordinator
# - this device controller does not require external code to maintain a connection, handle errors, and auto-reboot its device
# - upon encountering an error, this device controller (after handling the error) sends a notification and status update to its coordinator

# coordinator sees: available commands, an auto-updated status, and notifications to be logged

from abc import ABC, abstractmethod
import asyncio

class Device(ABC):

    def __init__(self, name):
        self.name = name
        self.active = False

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value

    @abstractmethod
    async def connect(self):
        '''connect to the lightbulb if necessary, throws error if fail'''
        pass

    @abstractmethod
    async def disconnect(self):
        '''disconnect from the lightbulb if available'''
        pass

    @abstractmethod
    async def turn_on(self):
        pass

    @abstractmethod
    async def turn_off(self):
        pass

    @abstractmethod
    async def set_brightness(self, brightness: int):
        '''brightness from 0-100, if available. returns False if unavailable'''
        pass

    @abstractmethod
    async def set_rgb(self, r: int, g: int, b: int):
        '''rgb, if available. returns False if unavailable'''
        pass

    @abstractmethod
    async def test_connection(self):
        '''throws error if disconnected'''
        pass

    @abstractmethod
    async def status(self):
        '''returns status (on/off)'''
        pass

    @abstractmethod
    async def repeated_flahes(self, on_off: bool):
        '''flashes repeatedly, if available (not safe for power switches)'''
        pass

