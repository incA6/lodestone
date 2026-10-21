# base class for all lightbulb controller types

from abc import ABC, abstractmethod

class lightbulb_controller(ABC):
    @abstractmethod
    def connect_and_stay_connected(self):
        '''connect to the lightbulb if necessary, throws error if disconnect'''
        pass

    @abstractmethod
    def disconnect(self):
        '''connect to the lightbulb if available'''
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def set_brightness(self, brightness: int):
        '''brightness from 0-100, if available. returns False if unavailable'''
        pass

    @abstractmethod
    def set_rgb(self, r: int, g: int, b: int):
        '''rgb, if available. returns False if unavailable'''
        pass

    @abstractmethod
    def is_connected(self):
        '''returns status of if lightbulb is connected'''
        pass

    @abstractmethod
    def status(self):
        '''returns status (on/off)'''
        pass

    @abstractmethod
    def repeated_flahes(self, on_off: bool):
        '''flashes repeatedly, if available (not safe for power switches)'''
        pass

