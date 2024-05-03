
import tkinter as tk
import os

from utils import ioutils, pyutils, guiutils

from ..abstracts import Panel
from .. import events


class BlankPanel(Panel):
    _ZERO_WIDTH_SPACE = "​"

    _LABEL_COLOR = "#858383"

    @classmethod
    def title(cls):
        # A zero-width space is returned such that the label frame pads the top of the frame as if it
        # contained text, matching the padding of the adjacent panel.
        return cls._ZERO_WIDTH_SPACE

    def __init__(self, parent, label=None):
        super().__init__(parent)
        self._init_label(label)

    def _init_label(self, content):
        if content is None:
            return
        text = str(content)
        if text:
            label = tk.Label(self._frame, text=text, fg=self._LABEL_COLOR)
            label.place(anchor=tk.CENTER, relx=0.5, rely=0.5)


class ToolPanel(Panel):

    _EVENT_STREAM = events.EventStream()

    _TITLE = "Tools"
    _MANIFEST_FILENAME = "MANIFEST"
    _ICON_SIZE = 35  # Pixels

    _NAME_KEY = "name"
    _ICON_KEY = "icon"
    _MODULE_KEY = "content"
    _PRIMARY_KEY = "first"
    _SECONDARY_KEY = "second"
    _TERTIARY_KEY = "third"

    _PANEL_KEYS = (
        _PRIMARY_KEY,
        _SECONDARY_KEY,
        _TERTIARY_KEY
    )

    @classmethod
    def title(cls):
        return cls._TITLE

    def __init__(self, parent, modules_dir):
        super().__init__(parent)
        self._icons = []  # Maintains references to icons such that they are not garbage collected
        self._buttons = self._init_buttons(modules_dir)

    def _init_buttons(self, modules):
        buttons = []
        for subdir in ioutils.absolute_subdirectories(modules):
            if ioutils.is_in_directory(self._MANIFEST_FILENAME, subdir):
                manifest_path = os.path.join(subdir, self._MANIFEST_FILENAME)
                button = self._build_button(manifest_path)
                button.pack(fill=tk.X)
                buttons.append(button)
        return buttons

    def _build_button(self, manifest_path):
        manifest = ioutils.read_config(manifest_path)
        primary_cls, secondary_cls, tertiary_cls = self._gather_panel_classes(manifest)
        command = self._build_button_command(
            primary_panel_cls=primary_cls,
            secondary_panel_cls=secondary_cls,
            tertiary_panel_cls=tertiary_cls
        )
        icon = self._build_icon(manifest[self._ICON_KEY])
        return tk.Button(
            self._frame,
            text=manifest[self._NAME_KEY],
            image=icon,
            compound=tk.LEFT,
            command=command
        )

    def _gather_panel_classes(self, manifest):
        output = []
        module = ioutils.import_module_from_source(manifest[self._MODULE_KEY])
        for key in self._PANEL_KEYS:
            cls_name = ioutils.value_if_mapped(manifest, key)
            cls = pyutils.getattr_if_present(module, cls_name)
            output.append(cls)
        return output

    def _build_button_command(self, primary_panel_cls=None, secondary_panel_cls=None, tertiary_panel_cls=None):
        primary_update = self._build_panel_update_function(events.UPDATE_PRIMARY_PANEL, primary_panel_cls)
        secondary_update = self._build_panel_update_function(events.UPDATE_SECONDARY_PANEL, secondary_panel_cls)
        tertiary_update = self._build_panel_update_function(events.UPDATE_TERTIARY_PANEL, tertiary_panel_cls)
        return pyutils.invoke(
            primary_update,
            secondary_update,
            tertiary_update
        )

    def _build_icon(self, path):
        icon = guiutils.build_icon(
            path,
            self._ICON_SIZE,
            self._ICON_SIZE
        )
        self._icons.append(icon)
        return icon

    def _build_panel_update_function(self, event, panel_cls):
        if pyutils.is_valid_subclass(panel_cls, Panel) and event in events.PANEL_UPDATE_EVENTS:
            return pyutils.package(self._EVENT_STREAM.publish, event, panel_cls)
        else:
            return pyutils.ignore
