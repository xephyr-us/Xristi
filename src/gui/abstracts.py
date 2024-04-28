import tkinter as tk
import abc


class WidgetWrapper(abc.ABC):

    _ATTR_ERR_MSG = "No attribute {} found in class {}"

    def __init__(self, widget_cls, parent):
        self._wrapped = widget_cls(parent)

    def __getattr__(self, item):
        try:
            return getattr(self._wrapped, item)
        except AttributeError:
            msg = self._ATTR_ERR_MSG.format(str(item), self.__class__.__name__)
            raise AttributeError(msg)


class Panel(WidgetWrapper, metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def title(cls):
        pass

    def __init__(self, parent):
        super().__init__(tk.Frame, parent)
        self._frame = self._wrapped
