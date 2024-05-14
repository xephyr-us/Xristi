
class Registrar:

    _NULL_THRESHOLD = 20

    _NULL_VALUE_ERR_MSG = "{} cannot accept null values"
    _NULL_TAG_ERR_MSG = "Values cannot be tagged with null inside {}"

    def __init__(self, *args):
        self._size = 0
        self._deletions = 0
        self._values = []
        self._indices = {}
        self._tags = {}
        for arg in args:
            self.register(arg)

    def __iter__(self):
        return _RegistrarIterator(self._values)

    def __len__(self):
        return self._size - self._deletions

    def __contains__(self, item):
        return item in self._indices.keys()

    def _validate_value(self, v):
        if v is None:
            msg = self._NULL_VALUE_ERR_MSG.format(self.__class__.__name__)
            raise ValueError(msg)

    def _validate_tag(self, t):
        if t is None:
            msg = self._NULL_TAG_ERR_MSG.format(self.__class__.__name__)
            raise ValueError(msg)

    def _tag_index(self, i, tags):
        for tag in tags:
            self._validate_tag(tag)
            self._tags.setdefault(tag, [])
            self._tags[tag].append(i)

    def _consolidate_data(self):
        old = self._values
        self.clear()
        for value in _RegistrarIterator(old):
            self.register(value)

    def clear(self):
        self._size = 0
        self._deletions = 0
        self._values = []
        self._indices = {}
        self._tags = {}

    def register(self, value, *tags):
        self._validate_value(value)
        self._values.append(value)
        index = self._size
        self._size += 1
        self._indices[value] = index
        self._tag_index(index, tags)

    def deregister(self, value):
        if value in self:
            index = self._indices[value]
            del self._indices[value]
            self._values[index] = None
            self._deletions += 1
            if self._deletions >= self._NULL_THRESHOLD:
                self._consolidate_data()

    def collect(self, tag):
        output = []
        if tag in self._tags.keys():
            indices = self._tags[tag]
            for i in indices:
                value = self._values[i]
                if value is not None:
                    output.append(value)
        return output

    def is_tagged(self, value, tag):
        if value not in self:
            return None
        if tag not in self._tags.keys():
            return False
        return self._indices[value] in self._tags[tag]


class _RegistrarIterator:

    def __init__(self, values):
        self._values = values
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        value = None
        try:
            while value is None:
                value = self._values[self._current]
                self._current += 1
            return value
        except IndexError:
            raise StopIteration
