
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

    # Relative to _GRID_SIZE
    _BUTTON_WIDTH = 1
    _TITLE_WIDTH = _GRID_SIZE - (2 * _BUTTON_WIDTH)
    _TITLE_HEIGHT = 15

    _TITLE_FONT = ("Consolas", 14, "bold")
    _SUBTITLE_FONT = ("Consolas", 11, "bold")
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
        self._delete_button = self._init_delete_button()
        self._complete_button = self._init_complete_button()

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
    
    def _init_delete_button(self):
        return guiutils.init_grid_widget( 
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH + 1,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            image=guiutils.build_icon(self._TRASH_PNG_PATH),
            command=self._delete
        )

    def _init_complete_button(self):
        return guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            x=self._TITLE_WIDTH,
            h=self._GRID_SIZE,
            w=self._BUTTON_WIDTH,
            image=guiutils.build_icon(self._CHECK_PNG_PATH),
            command=self._complete
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
        del self

    def _complete(self):
        self._EVENT_STREAM.publish(Events.COMPLETE_TASK, self)
        self._complete_button.grid_forget()


class ScrollableFrame(WidgetWrapper):

    _GRID_SIZE = 50
    _SCROLLBAR_WIDTH = 1

    def __init__(self, parent, *args, **kwargs):
        super().__init__(tk.Frame, parent, *args, **kwargs)
        self._outer_frame = self._wrapped
        guiutils.configure_grid(
            self._outer_frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._canvas = self._init_canvas()
        self._inner_frame = tk.Frame(self._canvas)
        self._scrollbar = self._init_scrollbar()
        self._config_scrolling()

    def _init_canvas(self):
        canvas = guiutils.init_grid_widget(
            tk.Canvas,
            self._outer_frame,
            borderwidth=0,
            w=self._GRID_SIZE - self._SCROLLBAR_WIDTH,
            h=self._GRID_SIZE,
            propagate=True
        )
        return canvas
    
    def _init_scrollbar(self):
        scrollbar = guiutils.init_grid_widget(
            tk.Scrollbar,
            self._outer_frame,
            orient=tk.VERTICAL,
            command=self._canvas.yview,
            x=self._GRID_SIZE - self._SCROLLBAR_WIDTH,
            w=self._SCROLLBAR_WIDTH,
            h=self._GRID_SIZE
        )
        return scrollbar
    
    def _config_scrolling(self):
        self._canvas.config(yscrollcommand=self._scrollbar.set)
        self._canvas.create_window(
            (4, 4), 
            window=self._inner_frame, 
            anchor="nw",
        )

        def on_frame_config():
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

        def on_canvas_config():
            self._canvas.create_window(
                (4, 4), 
                window=self._inner_frame, 
                anchor="nw",
                width=self._canvas.winfo_width()
            )

        self._inner_frame.bind("<Configure>", lambda _: on_frame_config())
        self._canvas.bind("<Configure>", lambda _: on_canvas_config())

    @property
    def frame(self):
        return self._inner_frame
    