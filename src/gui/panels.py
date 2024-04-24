
import tkinter as tk

from .mixins import Panel


class ToolPanel(Panel):

    @classmethod
    def title(cls):
        return "Tools"

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="red")


class BlankPanel(Panel):

    @classmethod
    def title(cls):
        return "Blank"

    def __init__(self, parent):
        super().__init__(parent)

