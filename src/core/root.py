
import tkinter as tk

from utils.pyutils import Reference, is_valid_subclass
from ..event_handling import EventStream, Events
from utils import ioutils, guiutils
from .. import abstracts

from . import panels


class RootWindow:
    """
    The root window of the Xristi application.
    """

    _EVENT_STREAM = EventStream()

    _GRID_WIDTH = 50
    _GRID_HEIGHT = 50

    # Relative to _GRID_WIDTH and _GRID_HEIGHT
    _PRIMARY_PANEL_WIDTH = 8
    _PRIMARY_PANEL_HEIGHT = 24
    _SECONDARY_PANEL_WIDTH = _PRIMARY_PANEL_WIDTH
    _SECONDARY_PANEL_HEIGHT = _GRID_HEIGHT - _PRIMARY_PANEL_HEIGHT
    _TERTIARY_PANEL_WIDTH = _GRID_WIDTH - _PRIMARY_PANEL_WIDTH
    _TERTIARY_PANEL_HEIGHT = _GRID_HEIGHT

    # Pixels
    _PANEL_PAD_X = 3
    _PANEL_PAD_Y = 3
    _ICON_SIZE = 50
    
    _PANEL_SUBCLS_ERR_MSG = "Class {} is not a subclass of {}"
    _BLANK_PANEL_MSG = "Select a tool to begin"

    _MODULES_PATH_KEY = "modules"
    _MIN_GEOMETRY_KEY = "mingeo"
    _GEOMETRY_KEY = "geo"
    _TITLE_KEY = "title"
    _ICON_KEY = "icon"

    @staticmethod
    def _primary_panel_keygen(panel_cls):
        return f"{panel_cls.__name__}1"

    @staticmethod
    def _secondary_panel_keygen(panel_cls):
        return f"{panel_cls.__name__}2"

    @staticmethod
    def _tertiary_panel_keygen(panel_cls):
        return f"{panel_cls.__name__}3"

    def __init__(self, config):
        self._config_path = config
        self._config = {}
        self._cache = {}
        self._relaunch = False
        self._root = None
        self._primary_panel_ref = Reference()
        self._secondary_panel_ref = Reference()
        self._tertiary_panel_ref = Reference()
        self._subscribe_to_events()

    def _initialize(self):
        self._clear_cached_values()
        self._relaunch = False
        self._config = ioutils.read_config(self._config_path)
        self._root = self._init_root()
        self._EVENT_STREAM.publish(Events.SET_PRIMARY_PANEL, panels.ToolPanel, self._config[self._MODULES_PATH_KEY])
        self._EVENT_STREAM.publish(Events.SET_SECONDARY_PANEL, panels.BlankPanel)
        self._EVENT_STREAM.publish(Events.SET_TERTIARY_PANEL, panels.BlankPanel, self._BLANK_PANEL_MSG)

    def _init_root(self):
        root = tk.Tk()
        root.title(self._config[self._TITLE_KEY])
        root.geometry(self._config[self._GEOMETRY_KEY])
        root.minsize(*self._get_mingeo())
        icon = guiutils.build_icon(self._config[self._ICON_KEY])
        root.iconphoto(True, icon)
        guiutils.configure_grid(root, self._GRID_WIDTH, self._GRID_HEIGHT)
        return root

    def _init_panel(self, panel_cls, panel_ref, keygen, *args, x=0, y=0, w=0, h=0, **kwargs):
        if not isinstance(panel_ref, Reference) or isinstance(panel_ref(), panel_cls):
            return
        if panel_ref() is not None:
            panel_ref().grid_forget()
        panel = self._get_cachable_panel(
            panel_cls,
            keygen(panel_cls),
            *args,
            *kwargs
        )
        panel.grid(
            column=x,
            row=y,
            columnspan=w,
            rowspan=h,
            padx=self._PANEL_PAD_X,
            pady=self._PANEL_PAD_Y,
            sticky="NSEW"
        )
        panel.grid_propagate(0)
        panel_ref(panel)

    def _subscribe_to_events(self):
        self._EVENT_STREAM.subscribe(Events.SET_PRIMARY_PANEL, self._set_primary_panel)
        self._EVENT_STREAM.subscribe(Events.SET_SECONDARY_PANEL, self._set_secondary_panel)
        self._EVENT_STREAM.subscribe(Events.SET_TERTIARY_PANEL, self._set_tertiary_panel)

    def _clear_cached_values(self):
        self._config.clear()
        self._cache.clear()
        self._root = None
        self._primary_panel_ref(None)
        self._secondary_panel_ref(None)
        self._tertiary_panel_ref(None)

    def _get_geo(self):
        return tuple(
            int(x) for x in self._config[self._GEOMETRY_KEY].split("x")
        )

    def _get_mingeo(self):
        return tuple(
            int(x) for x in self._config[self._MIN_GEOMETRY_KEY].split("x")
        )

    def _set_primary_panel(self, panel_cls, *args, **kwargs):
        self._init_panel(
            panel_cls,
            self._primary_panel_ref,
            self._primary_panel_keygen,
            *args,
            x=0,
            y=0,
            w=self._PRIMARY_PANEL_WIDTH,
            h=self._PRIMARY_PANEL_HEIGHT,
            **kwargs
        )

    def _set_secondary_panel(self, panel_cls, *args, **kwargs):
        self._init_panel(
            panel_cls,
            self._secondary_panel_ref,
            self._secondary_panel_keygen,
            *args,
            x=0,
            y=self._PRIMARY_PANEL_HEIGHT,
            w=self._SECONDARY_PANEL_WIDTH,
            h=self._SECONDARY_PANEL_HEIGHT,
            **kwargs
        )

    def _set_tertiary_panel(self, panel_cls, *args, **kwargs):
        self._init_panel(
            panel_cls,
            self._tertiary_panel_ref,
            self._tertiary_panel_keygen,
            *args,
            x=self._PRIMARY_PANEL_WIDTH,
            y=0,
            w=self._TERTIARY_PANEL_WIDTH,
            h=self._TERTIARY_PANEL_HEIGHT,
            **kwargs
        )

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
        if not is_valid_subclass(panel_cls, abstracts.Panel):
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
