
import tkinter as tk
import os

from utils import ioutils, pyutils
from .mixins import Panel
from .. import events


class BlankPanel(Panel):

    _LABEL_COLOR = "#858383"

    _ZERO_WIDTH_SPACE = "​"

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

    _MODULE_DEF_FILENAME = "MANIFEST"

    @classmethod
    def title(cls):
        return "Tools"

    def __init__(self, parent, modules_dir):
        super().__init__(parent)
        self._buttons = self._init_buttons(modules_dir)

    def _init_buttons(self, modules):
        buttons = []
        for subdir in ioutils.absolute_subdirectories(modules):
            if ioutils.is_in_directory(self._MODULE_DEF_FILENAME, subdir):
                module = os.path.join(subdir, self._MODULE_DEF_FILENAME)
                button = self._build_button(module)
                button.pack(fill=tk.X)
                buttons.append(button)
        return buttons

    def _build_button(self, module):
        definition = ioutils.read_key_value_file(module, extend_filepaths=True)
        command = pyutils.package(
            self._EVENT_STREAM.publish,
            events.UPDATE_TERTIARY_PANEL,
            BlankPanel,
            definition["name"]
        )
        return tk.Button(
            self._frame,
            text=definition["name"],
            command=command
        )
