
import tkinter as tk

import utils.customio as ioutil
from . import panels


class RootWindow:

    _TITLE_KEY = "TITLE"
    _GEOMETRY_KEY = "GEO"
    _TOOLS_KEY = "TOOLS"

    _GRID_WIDTH = 50
    _GRID_HEIGHT = 50

    _TOOL_PANEL_WIDTH = 11
    _TOOL_PANEL_HEIGHT = 24

    def __init__(self, config):
        self._config_path = config
        self._config = ioutil.read_key_value_file(config)
        self._root = self._init_root()
        self._configure_grid()
        self._tool_panel = self._init_tool_panel()
        self._major_panel = self._init_major_panel()
        self._minor_panel = self._init_minor_panel()

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        return root

    def _init_tool_panel(self):
        panel = panels.ToolPanel(self._root)
        panel.grid(
            row=0,
            column=0,
            rowspan=self._TOOL_PANEL_HEIGHT,
            columnspan=self._TOOL_PANEL_WIDTH,
            sticky=tk.NSEW
        )
        return panel

    def _init_major_panel(self):
        panel = panels.MajorPanel(self._root)
        panel.grid(
            row=0,
            column=self._TOOL_PANEL_WIDTH,
            rowspan=self._GRID_HEIGHT,
            columnspan=self._GRID_WIDTH - self._TOOL_PANEL_WIDTH,
            sticky=tk.NSEW
        )
        return panel

    def _init_minor_panel(self):
        panel = panels.MinorPanel(self._root)
        panel.grid(
            row=self._TOOL_PANEL_HEIGHT,
            column=0,
            rowspan=self._GRID_HEIGHT - self._TOOL_PANEL_HEIGHT,
            columnspan=self._TOOL_PANEL_WIDTH,
            sticky=tk.NSEW
        )
        return panel

    def _configure_grid(self):
        for x in range(self._GRID_WIDTH):
            self._root.rowconfigure(x, weight=1)
        for y in range(self._GRID_HEIGHT):
            self._root.columnconfigure(y, weight=1)

    def launch(self):
        self._root.mainloop()
        return False
