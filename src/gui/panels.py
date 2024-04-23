import tkinter as tk
from abc import ABC


class Panel(ABC):

    _ATTR_ERR_MSG = "No attribute {} found in class {}"

    def __init__(self, parent):
        self._frame = tk.Frame(parent)

    def __getattr__(self, item):
        try:
            attr = getattr(self._frame, item)
            return attr
        except AttributeError:
            msg = self._ATTR_ERR_MSG.format(str(item), self.__class__.__name__)
            raise AttributeError(msg)


class ToolPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="red")


class MajorPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="blue")


class MinorPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="green")
