
import tkinter as tk

# Imported for reference by MANIFEST
from src.core.panels import BlankPanel

from src.abstracts import Panel


class ToDoPanel(Panel):

    _TITLE = "To-do List"

    def __init__(self, parent):
        super().__init__(parent)
        self._init_label("To-do Lists")

    def _init_label(self, text):
        label = tk.Label(self._frame, text=text, fg="purple")
        label.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
