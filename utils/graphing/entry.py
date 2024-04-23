
class SleepEntry:

    def __init__(self, title, start, length):
        self._title = title
        self._start = start
        self._length = length

    @property
    def title(self):
        return self._title

    @property
    def start(self):
        return self._start

    @property
    def length(self):
        return self._length
