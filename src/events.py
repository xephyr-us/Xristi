
UPDATE_PRIMARY_PANEL = 0
UPDATE_SECONDARY_PANEL = 1
UPDATE_TERTIARY_PANEL = 2

PANEL_UPDATE_EVENTS = {
    UPDATE_PRIMARY_PANEL,
    UPDATE_SECONDARY_PANEL,
    UPDATE_TERTIARY_PANEL
}


class EventStream:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventStream, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__mappings = {}

    def publish(self, event, *args, **kwargs):
        if event in self.__mappings.keys():
            subscribers = self.__mappings[event]
            for func in subscribers:
                func(*args, **kwargs)

    def subscribe(self, event, func):
        self.__mappings.setdefault(event, [])
        self.__mappings[event].append(func)
