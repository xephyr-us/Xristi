
def package(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def invoke(*funcs):
    def wrapper(*args, **kwargs):
        for func in funcs:
            func(*args, **kwargs)
    return wrapper


def ignore(*args, **kwargs):
    return
