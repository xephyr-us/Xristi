
import tkinter as tk

from utils import ioutils

# Imported for reference by MANIFEST
from src.core.panels import BlankPanel
from src.abstracts import Panel


class BlockPanel(Panel):

    @classmethod
    def title(cls):
        return "Blocklist"

    def __init__(self, parent):
        super().__init__(parent)
        self._init_label("Blocked Sites")
        print(ioutils.get_cwd())

    def _init_label(self, text):
        label = tk.Label(self._frame, text=text, fg="red")
        label.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
