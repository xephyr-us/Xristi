
import tkinter as tk

from utils import ioutils, guiutils
from .. import events

from . import panels, abstracts


class RootWindow:

    _EVENT_STREAM = events.EventStream()

    _GRID_WIDTH = 50
    _GRID_HEIGHT = 50

    _PRIMARY_PANEL_WIDTH = 11   # Relative to _GRID_WIDTH
    _PRIMARY_PANEL_HEIGHT = 24  # Relative to _GRID_HEIGHT

    # Pixels
    _PANEL_PAD_X = 3
    _PANEL_PAD_Y = 3
    _ICON_SIZE = 50

    _PANEL_SUBCLS_ERR_MSG = "Class {} is not a subclass of {}"
    _BLANK_PANEL_MSG = "Select a tool to begin"

    _TITLE_KEY = "title"
    _GEOMETRY_KEY = "geo"
    _ICON_KEY = "icon"
    _TOOLS_KEY = "tools"

    def __init__(self, config):
        self._config_path = config
        self._relaunch = False
        self._config = None
        self._root = None
        self._primary_panel = None
        self._secondary_panel = None
        self._tertiary_panel = None
        self._subscribe_to_events()

    def _initialize(self):
        self._relaunch = False
        self._config = ioutils.read_config(self._config_path)
        self._root = self._init_root()

    def _subscribe_to_events(self):
        self._EVENT_STREAM.subscribe(events.UPDATE_PRIMARY_PANEL, self._set_primary_panel)
        self._EVENT_STREAM.subscribe(events.UPDATE_SECONDARY_PANEL, self._set_secondary_panel)
        self._EVENT_STREAM.subscribe(events.UPDATE_TERTIARY_PANEL, self._set_tertiary_panel)

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        icon = guiutils.build_icon(
            self._config[self._ICON_KEY],
            self._ICON_SIZE,
            self._ICON_SIZE
        )
        root.iconphoto(True, icon)
        guiutils.configure_grid(root, self._GRID_WIDTH, self._GRID_HEIGHT)
        return root

    def _set_primary_panel(self, panel_cls, *args, **kwargs):
        self._verify_panel_class(panel_cls)
        panel = guiutils.init_labeled_grid_widget(
            panel_cls,
            self._root,
            panel_cls.title(),
            *args,
            x=0,
            y=0,
            w=self._PRIMARY_PANEL_WIDTH,
            h=self._PRIMARY_PANEL_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            **kwargs
        )
        self._primary_panel = panel

    def _set_secondary_panel(self, panel_cls, *args, **kwargs):
        self._verify_panel_class(panel_cls)
        panel = guiutils.init_labeled_grid_widget(
            panel_cls,
            self._root,
            panel_cls.title(),
            *args,
            x=0,
            y=self._PRIMARY_PANEL_HEIGHT,
            w=self._PRIMARY_PANEL_WIDTH,
            h=self._GRID_HEIGHT - self._PRIMARY_PANEL_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            **kwargs
        )
        self._secondary_panel = panel

    def _set_tertiary_panel(self, panel_cls, *args, **kwargs):
        self._verify_panel_class(panel_cls)
        panel = guiutils.init_labeled_grid_widget(
            panel_cls,
            self._root,
            panel_cls.title(),
            *args,
            x=self._PRIMARY_PANEL_WIDTH,
            y=0,
            w=self._GRID_WIDTH - self._PRIMARY_PANEL_WIDTH,
            h=self._GRID_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            **kwargs
        )
        self._tertiary_panel = panel

    def _verify_panel_class(self, panel_cls):
        if not issubclass(panel_cls, abstracts.Panel):
            msg = self._PANEL_SUBCLS_ERR_MSG.format(
                panel_cls.__name__,
                abstracts.Panel.__name__
            )
            raise TypeError(msg)

    def launch(self):
        self._initialize()
        self._EVENT_STREAM.publish(events.UPDATE_PRIMARY_PANEL, panels.ToolPanel, self._config[self._TOOLS_KEY])
        self._EVENT_STREAM.publish(events.UPDATE_SECONDARY_PANEL, panels.BlankPanel)
        self._EVENT_STREAM.publish(events.UPDATE_TERTIARY_PANEL, panels.BlankPanel, self._BLANK_PANEL_MSG)
        self._root.mainloop()
        self._root.quit()
        return self._relaunch
