
ZERO_WIDTH_SPACE = "​"


def package(func, *args, **kwargs):
    """
    Produces a function object which, when called, calls the func with the given arguments.
    """
    return lambda: func(*args, **kwargs)


def invoke(*funcs):
    """
    Produces a function object which, when called, invokes all given functions in sequence with the given arguments.
    """
    def wrapper(*args, **kwargs):
        for func in funcs:
            func(*args, **kwargs)
    return wrapper


def ignore(*args, **kwargs):
    """
    Does nothing.
    """
    return


def getattr_if_present(obj, attr):
    """
    Returns None if the attribute attr doesn't exist within obj; returns the attributed value otherwise.
    """
    try:
        if obj is None or attr is None:
            raise AttributeError
        return getattr(obj, attr)
    except AttributeError:
        return None


def is_valid_subclass(cls, supercls):
    """
    Returns False if cls is None or cls is not a subclass of supercls. Returns True otherwise.
    """
    return cls is not None and issubclass(cls, supercls)


class Reference:
    """
    Acts as a reference to an arbitrary object. Used to produce pass-by-reference behavior.
    """

    def __init__(self, value=None):
        self._value = value

    def __call__(self, *args):
        length = len(args)
        if length == 0:
            return self._value
        elif length == 1:
            self._value = args[0]
        else:
            self._value = [a for a in args]

    def get(self):
        return self._value

    def set(self, value):
        self._value = value
