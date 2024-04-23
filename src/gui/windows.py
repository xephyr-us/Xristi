
import tkinter as tk

import utils.customio as ioutil
from . import panels


class RootWindow:

    _TITLE_KEY = "TITLE"
    _GEOMETRY_KEY = "GEO"
    _TOOLS_KEY = "TOOLS"

    def __init__(self, config):
        self._config_path = config
        self._config = ioutil.read_key_value_file(config)
        self._root = self._init_root()
        self._tool_panel = self._init_panel()

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        return root

    def _init_panel(self):
        panel = panels.ToolPanel(self._root)
        panel.grid(row=0, column=0, sticky=tk.NSEW)
        return panel

    def launch(self):
        self._root.mainloop()
        return False
