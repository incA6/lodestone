# base class for all lightbulb controller types
# throws errors for Lighting to catch and log

from abc import ABC, abstractmethod
import asyncio

class LightbulbController(ABC):

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
        '''returns status of if lightbulb is connected, if available'''
        pass

    @abstractmethod
    async def status(self):
        '''returns status (on/off)'''
        pass

    @abstractmethod
    async def repeated_flahes(self, on_off: bool):
        '''flashes repeatedly, if available (not safe for power switches)'''
        pass

