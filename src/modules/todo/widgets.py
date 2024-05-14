
import tkinter as tk

from src.abstracts import WidgetWrapper


class TaskWidget(WidgetWrapper):

    def __init__(self, parent, name):
        super().__init__(tk.LabelFrame, parent)
        label = tk.Label(self._wrapped, text=name)
        label.pack(fill=tk.Y, anchor="w")
