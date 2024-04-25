
def package(func, *arg, **kwargs):
    def wrapper():
        func(*arg, **kwargs)
    return wrapper
