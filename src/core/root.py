
import tkinter as tk

from ..event_handling import EventStream, Events
from utils import ioutils, guiutils
from .. import abstracts

from . import panels


class RootWindow:

    _EVENT_STREAM = EventStream()

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

    _MODULES_PATH_KEY = "modules"
    _GEOMETRY_KEY = "geo"
    _TITLE_KEY = "title"
    _ICON_KEY = "icon"

    @staticmethod
    def _primary_panel_key(panel_cls):
        return f"{panel_cls.__name__}1"

    @staticmethod
    def _secondary_panel_key(panel_cls):
        return f"{panel_cls.__name__}2"

    @staticmethod
    def _tertiary_panel_key(panel_cls):
        return f"{panel_cls.__name__}3"

    def __init__(self, config):
        self._config_path = config
        self._config = {}
        self._cache = {}
        self._relaunch = False
        self._root = None
        self._primary_panel = None
        self._secondary_panel = None
        self._tertiary_panel = None
        self._subscribe_to_events()

    def _initialize(self):
        self._clear_cached_values()
        self._relaunch = False
        self._config = ioutils.read_config(self._config_path)
        self._root = self._init_root()
        self._EVENT_STREAM.publish(Events.UPDATE_PRIMARY_PANEL, panels.ToolPanel, self._config[self._MODULES_PATH_KEY])
        self._EVENT_STREAM.publish(Events.UPDATE_SECONDARY_PANEL, panels.BlankPanel)
        self._EVENT_STREAM.publish(Events.UPDATE_TERTIARY_PANEL, panels.BlankPanel, self._BLANK_PANEL_MSG)

    def _subscribe_to_events(self):
        self._EVENT_STREAM.subscribe(Events.UPDATE_PRIMARY_PANEL, self._set_primary_panel)
        self._EVENT_STREAM.subscribe(Events.UPDATE_SECONDARY_PANEL, self._set_secondary_panel)
        self._EVENT_STREAM.subscribe(Events.UPDATE_TERTIARY_PANEL, self._set_tertiary_panel)

    def _clear_cached_values(self):
        self._config.clear()
        self._cache.clear()
        self._root = None
        self._primary_panel = None
        self._secondary_panel = None
        self._tertiary_panel = None

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

    def _init_panel(self, panel_cls, current_panel, *args, **kwargs):
        if isinstance(current_panel, panel_cls):
            return
        self._verify_panel_class(panel_cls)
        if current_panel is not None:
            current_panel.grid_forget()
        new_panel = self._get_cachable_panel(panel_cls, "KEY", *args, **kwargs)
        new_panel.grid(
            # **(Current panel coords)
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            sticky=tk.NSEW
        )
        # Update panel reference

    def _set_primary_panel(self, panel_cls, *args, **kwargs):
        if isinstance(self._primary_panel, panel_cls):
            return
        if self._primary_panel is not None:
            self._primary_panel.master.grid_forget()
        panel = self._get_cachable_panel(panel_cls, self._primary_panel_key(panel_cls), *args, **kwargs)
        panel.grid(
            column=0,
            row=0,
            columnspan=self._PRIMARY_PANEL_WIDTH,
            rowspan=self._PRIMARY_PANEL_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            sticky=tk.NSEW
        )
        self._primary_panel = panel

    def _set_secondary_panel(self, panel_cls, *args, **kwargs):
        if isinstance(self._secondary_panel, panel_cls):
            return
        if self._secondary_panel is not None:
            self._secondary_panel.master.grid_forget()
        panel = self._get_cachable_panel(panel_cls, self._secondary_panel_key(panel_cls), *args, **kwargs)
        panel.grid(
            column=0,
            row=self._PRIMARY_PANEL_HEIGHT,
            columnspan=self._PRIMARY_PANEL_WIDTH,
            rowspan=self._GRID_HEIGHT - self._PRIMARY_PANEL_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            sticky=tk.NSEW
        )
        self._secondary_panel = panel

    def _set_tertiary_panel(self, panel_cls, *args, **kwargs):
        if isinstance(self._tertiary_panel, panel_cls):
            return
        self._verify_panel_class(panel_cls)
        if self._tertiary_panel is not None:
            self._tertiary_panel.grid_forget()
        panel = self._get_cachable_panel(panel_cls, self._tertiary_panel_key(panel_cls), *args, **kwargs)
        panel.grid(
            column=self._PRIMARY_PANEL_WIDTH,
            row=0,
            columnspan=self._GRID_WIDTH - self._PRIMARY_PANEL_WIDTH,
            rowspan=self._GRID_HEIGHT,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            sticky=tk.NSEW
        )
        self._tertiary_panel = panel

    def _get_cachable_panel(self, panel_cls, cache_key, *args, **kwargs):
        self._verify_panel_class(panel_cls)
        cached = ioutils.value_if_mapped(self._cache, cache_key)
        if cached is not None:
            return cached
        panel = panel_cls(
            self._root,
            *args,
            **kwargs
        )
        self._cache[cache_key] = panel
        return panel

    def _verify_panel_class(self, panel_cls):
        if not issubclass(panel_cls, abstracts.Panel):
            msg = self._PANEL_SUBCLS_ERR_MSG.format(
                panel_cls.__name__,
                abstracts.Panel.__name__
            )
            raise TypeError(msg)

    def launch(self):
        self._initialize()
        self._root.mainloop()
        self._root.quit()
        return self._relaunch
