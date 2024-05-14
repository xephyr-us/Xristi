
import tkinter as tk

from utils.pyutils import ZERO_WIDTH_SPACE
from utils import guiutils

from src.abstracts import WidgetWrapper


class TaskWidget(WidgetWrapper):

    _GRID_SIZE = 20
    _BUTTON_WIDTH = 1
    _TITLE_WIDTH = _GRID_SIZE - (2 * _BUTTON_WIDTH)
    _TITLE_HEIGHT = 15

    _TITLE_FONT = ("Helvetica", 14, "bold")
    _SUBTITLE_FONT = ("Helvetica", 11)

    _DEFAULT_TITLE_COLOR = "#282829"
    _DEFAULT_SUBTITLE_COLOR = "#282829"

    @staticmethod
    def _validate_text(text):
        return text if text is not None and isinstance(text, str) else ZERO_WIDTH_SPACE

    def __init__(self, parent, title, subtitle=None, title_color=None, subtitle_color=None):
        super().__init__(tk.LabelFrame, parent)
        self._frame = self._wrapped
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._title = self._init_title(title, title_color)
        self._subtitle = self._init_subtitle(subtitle, subtitle_color)
        self._buttons = self._init_buttons()

    def _init_title(self, text, color):
        text = self._validate_text(text)
        label = guiutils.init_grid_widget(
            tk.Label,
            self._frame,
            x=0,
            y=0,
            w=self._TITLE_WIDTH,
            h=self._TITLE_HEIGHT,
            text=text,
            fg=color if color else self._DEFAULT_SUBTITLE_COLOR,
            font=self._TITLE_FONT,
            sticky=tk.W
        )
        return label

    def _init_subtitle(self, text, color):
        text = self._validate_text(text)
        label = guiutils.init_grid_widget(
            tk.Label,
            self._frame,
            x=0,
            y=self._TITLE_HEIGHT,
            w=self._TITLE_WIDTH,
            h=self._GRID_SIZE - self._TITLE_HEIGHT,
            text=text,
            fg=color if color else self._DEFAULT_SUBTITLE_COLOR,
            font=self._SUBTITLE_FONT,
            sticky=tk.W
        )
        return label

    def _init_buttons(self):
        complete_button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH,
            y=0,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            text="done",
        )
        delete_button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH + 1,
            y=0,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            text="trash",
            sticky=tk.E + tk.N + tk.S
        )
        return complete_button, delete_button
