
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
