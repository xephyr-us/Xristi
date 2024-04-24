
import tkinter as tk

from utils import ioutils, guiutils
from . import panels, mixins
from .. import events


class RootWindow:

    _EVENT_STREAM = events.EventStream()

    _TITLE_KEY = "TITLE"
    _GEOMETRY_KEY = "GEO"
    _TOOLS_KEY = "TOOLS"

    _GRID_WIDTH = 50
    _GRID_HEIGHT = 50

    _PRIMARY_PANEL_WIDTH = 11   # Relative to _GRID_WIDTH
    _PRIMARY_PANEL_HEIGHT = 24  # Relative to _GRID_HEIGHT

    def __init__(self, config):
        self._config_path = config
        self._config = ioutils.read_key_value_file(config)
        self._root = self._init_root()
        self._primary_panel = None
        self._secondary_panel = None
        self._tertiary_panel = None
        self._subscribe_to_events()

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        guiutils.configure_grid(root, self._GRID_WIDTH, self._GRID_HEIGHT)
        return root

    def _subscribe_to_events(self):
        self._EVENT_STREAM.subscribe(events.UPDATE_PRIMARY_PANEL, self._set_primary_panel)
        self._EVENT_STREAM.subscribe(events.UPDATE_SECONDARY_PANEL, self._set_secondary_panel)
        self._EVENT_STREAM.subscribe(events.UPDATE_TERTIARY_PANEL, self._set_tertiary_panel)

    def _set_primary_panel(self, panel_cls):
        panel = guiutils.init_grid_widget(
            panel_cls,
            self._root,
            x=0,
            y=0,
            w=self._PRIMARY_PANEL_WIDTH,
            h=self._PRIMARY_PANEL_HEIGHT
        )
        self._primary_panel = panel

    def _set_secondary_panel(self, panel_cls):
        panel = guiutils.init_grid_widget(
            panel_cls,
            self._root,
            x=0,
            y=self._PRIMARY_PANEL_HEIGHT,
            w=self._PRIMARY_PANEL_WIDTH,
            h=self._GRID_HEIGHT - self._PRIMARY_PANEL_HEIGHT
        )
        self._secondary_panel = panel

    def _set_tertiary_panel(self, panel_cls):
        panel = guiutils.init_grid_widget(
            panel_cls,
            self._root,
            x=self._PRIMARY_PANEL_WIDTH,
            y=0,
            w=self._GRID_WIDTH - self._PRIMARY_PANEL_WIDTH,
            h=self._GRID_HEIGHT
        )
        self._tertiary_panel = panel

    def launch(self):
        self._EVENT_STREAM.publish(events.UPDATE_PRIMARY_PANEL, panels.ToolPanel)
        self._EVENT_STREAM.publish(events.UPDATE_SECONDARY_PANEL, panels.BlankPanel)
        self._EVENT_STREAM.publish(events.UPDATE_TERTIARY_PANEL, panels.BlankPanel)
        self._root.mainloop()
        return False
