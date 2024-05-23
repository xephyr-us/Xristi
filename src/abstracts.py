
import tkinter as tk
import abc

from utils.pyutils import ZERO_WIDTH_SPACE


class Singleton(abc.ABC):
    """
    A mixin used to implement the singleton design pattern.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


class WidgetWrapper(abc.ABC):
    """
    A mixin allowing an object to extend the interface of its wrapped widget.
    """

    _INV_WIDGET_CLS_ERR_MSG = "Invalid widget class {} passed to {}"
    _ATTR_ERR_MSG = "No attribute {} found in class {}"

    def __init__(self, widget_cls, parent, *args, **kwargs):
        self._validate_widget_class(widget_cls)
        self._wrapped = widget_cls(parent, *args, **kwargs)

    def __getattr__(self, item):
        try:
            return getattr(self._wrapped, item)
        except AttributeError:
            msg = self._ATTR_ERR_MSG.format(str(item), self.__class__.__name__)
            raise AttributeError(msg)

    def _validate_widget_class(self, widget_cls):
        if not issubclass(widget_cls, tk.Widget):
            msg = self._INV_WIDGET_CLS_ERR_MSG.format(
                widget_cls.__name__,
                self.__class__.__name__
            )
            raise TypeError(msg)


class Panel(WidgetWrapper, metaclass=abc.ABCMeta):
    """
    An abstract class which wraps and titles a LabelFrame widget.
    """

    _TITLE = ZERO_WIDTH_SPACE
    # A zero-width space is used as the default title such that the empty label pads the top of the
    # frame as if it contained text, matching the padding of filled labels

    def __init__(self, parent, *args, **kwargs):
        super().__init__(tk.LabelFrame, parent, *args, **kwargs)
        self._frame = self._wrapped
        self._frame.config(text=self._TITLE)

    @property
    def title(self):
        return self._TITLE
