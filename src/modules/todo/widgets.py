
import tkinter as tk

from utils.pyutils import ZERO_WIDTH_SPACE, WHITESPACE
from src.event_handling import EventStream, Events
from src.abstracts import WidgetWrapper
from utils import guiutils


class TaskWidget(WidgetWrapper):
    """
    Represents a task on the user's todo list as a UI element.
    """

    _EVENT_STREAM = EventStream()

    _GRID_SIZE = 20
    _BUTTON_WIDTH = 1
    _TITLE_WIDTH = _GRID_SIZE - (2 * _BUTTON_WIDTH)
    _TITLE_HEIGHT = 15

    _TITLE_FONT = ("Consolas", 14, "bold")
    _SUBTITLE_FONT = ("Consolas", 11)
    _LABEL_LENGTH = 60  # Characters
    _LABEL_FG = "#282829"

    _TRASH_PNG_PATH = "./assets/trash.png"
    _CHECK_PNG_PATH = "./assets/check.png"

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
        self._init_buttons()

    def _init_title(self, text, color):
        normalized = self._normalize_text(text)
        label = guiutils.init_grid_widget(
            tk.Label,
            self._frame,
            x=0,
            y=0,
            w=self._TITLE_WIDTH,
            h=self._TITLE_HEIGHT,
            text=normalized,
            fg=color if color else self._LABEL_FG,
            font=self._TITLE_FONT,
            sticky=tk.W
        )
        return label

    def _init_subtitle(self, text, color):
        normalized = self._normalize_text(text)
        label = guiutils.init_grid_widget(
            tk.Label,
            self._frame,
            x=0,
            y=self._TITLE_HEIGHT,
            w=self._TITLE_WIDTH,
            h=self._GRID_SIZE - self._TITLE_HEIGHT,
            text=normalized,
            fg=color if color else self._LABEL_FG,
            font=self._SUBTITLE_FONT,
            sticky=tk.W
        )
        return label

    def _init_buttons(self):
        guiutils.init_grid_widget(  # Complete Button
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            image=guiutils.build_icon(self._CHECK_PNG_PATH),
            command=self._delete
        )
        guiutils.init_grid_widget(  # Delete Button
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH + 1,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            image=guiutils.build_icon(self._TRASH_PNG_PATH),
            command=self._delete
        )
    
    def _normalize_text(self, text):
        if text is None or not isinstance(text, str): 
            return ZERO_WIDTH_SPACE
        length = len(text)
        if length >= self._LABEL_LENGTH:
            return text[:self._LABEL_LENGTH]
        return text + WHITESPACE * (self._LABEL_LENGTH - length)
        
    def _delete(self):
        self._EVENT_STREAM.publish(Events.DEL_TASK, self)
        self.destroy()
