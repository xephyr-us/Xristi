
import tkinter as tk

from .mixins import Panel


class ToolPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        label = tk.LabelFrame(self._frame, text="Tools")
        label.pack(padx=5, pady=3, fill=tk.BOTH, expand=True)


class MajorPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        label = tk.LabelFrame(self._frame, text="Major")
        label.pack(padx=5, pady=3, fill=tk.BOTH, expand=True)


class MinorPanel(Panel):

    def __init__(self, parent):
        super().__init__(parent)
        label = tk.LabelFrame(self._frame, text="Minor")
        label.pack(padx=5, pady=3, fill=tk.BOTH, expand=True)
