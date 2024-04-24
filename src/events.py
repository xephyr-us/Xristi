
UPDATE_PRIMARY_PANEL = 1
UPDATE_SECONDARY_PANEL = 2
UPDATE_TERTIARY_PANEL = 3


class EventStream:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventStream, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__mappings = {}

    def publish(self, event, *args, **kwargs):
        subscribers = self.__mappings[event]
        for func in subscribers:
            func(*args, **kwargs)

    def subscribe(self, event, func):
        self.__mappings.setdefault(event, [])
        self.__mappings[event].append(func)
