
ZERO_WIDTH_SPACE = "​"


def package(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def invoke(*funcs):
    def wrapper(*args, **kwargs):
        for func in funcs:
            func(*args, **kwargs)
    return wrapper


def ignore(*args, **kwargs):
    return


def getattr_if_present(obj, attr):
    try:
        if obj is None or attr is None:
            raise AttributeError
        return getattr(obj, attr)
    except AttributeError:
        return None


def is_valid_subclass(cls, supercls):
    return cls is not None and issubclass(cls, supercls)


class Reference:

    def __init__(self, value=None):
        self._value = value

    def __call__(self, *args, **kwargs):
        if args:
            self._value = args[0]
        else:
            return self._value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
