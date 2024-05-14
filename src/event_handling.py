
from enum import Enum

from .abstracts import Singleton


class Events(Enum):
    SET_PRIMARY_PANEL = 0
    SET_SECONDARY_PANEL = 1
    SET_TERTIARY_PANEL = 2


class EventStream(Singleton):

    def __init__(self):
        self.__mappings = {}

    def publish(self, event, *args, **kwargs):
        if event in Events and event in self.__mappings.keys():
            subscribers = self.__mappings[event]
            for func in subscribers:
                func(*args, **kwargs)

    def subscribe(self, event, func):
        if event in Events:
            self.__mappings.setdefault(event, [])
            self.__mappings[event].append(func)
