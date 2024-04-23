
import tkinter as tk

import utils.customio as ioutil


class RootWindow:

    _TITLE_KEY = "TITLE"
    _GEOMETRY_KEY = "GEO"
    _TOOLS_KEY = "TOOLS"

    def __init__(self, config):
        self._config_path = config
        self._config = ioutil.read_key_value_file(config)
        self._root = self._init_root()

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        return root

    def launch(self):
        self._root.mainloop()
        return False
