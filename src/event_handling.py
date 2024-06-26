
from enum import Enum

from .abstracts import Singleton


class Events(Enum):
    """
    An enum specifying the integer codes by which handled events are referenced.
    """
    SET_PRIMARY_PANEL = 0
    SET_SECONDARY_PANEL = 1
    SET_TERTIARY_PANEL = 2
    NEW_TASK = 3
    DEL_TASK = 4
    COMPLETE_TASK = 5
    SET_TASK_TOPICS = 6
    SELECT_TASK_TOPIC = 7
    SELECT_TASKS_COMPLETED = 8


class EventStream(Singleton):
    """
    A singleton which implements the pubsub messaging pattern for handled events.
    """

    __mappings = {}

    def publish(self, event, *args, **kwargs):
        if event in Events and event in self.__mappings.keys():
            subscribers = self.__mappings[event]
            for func in subscribers:
                func(*args, **kwargs)

    def subscribe(self, event, func):
        if event in Events:
            self.__mappings.setdefault(event, [])
            self.__mappings[event].append(func)
