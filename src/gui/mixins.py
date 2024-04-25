import tkinter as tk
import abc


class Panel(abc.ABC):

    _ATTR_ERR_MSG = "No attribute {} found in class {}"

    @classmethod
    @abc.abstractmethod
    def title(cls):
        pass

    def __init__(self, parent):
        self._frame = tk.Frame(parent)

    def __getattr__(self, item):
        try:
            return getattr(self._frame, item)
        except AttributeError:
            msg = self._ATTR_ERR_MSG.format(str(item), self.__class__.__name__)
            raise AttributeError(msg)


class WrappedButton(abc.ABC):

    _ATTR_ERR_MSG = "No attribute {} found in class {}"

    def __init__(self, parent):
        self._button = tk.Button(parent)

    def __getattr__(self, item):
        try:
            return getattr(self._button, item)
        except AttributeError:
            msg = self._ATTR_ERR_MSG.format(str(item), self.__class__.__name__)
            raise AttributeError(msg)
