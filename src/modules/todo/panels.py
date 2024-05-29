
from tkinter import simpledialog as dialog
import tkinter as tk

from src.event_handling import EventStream, Events
from src.abstracts import Panel
from utils import guiutils

from src.modules.todo.structs import Registrar
from src.modules.todo import widgets


class TaskPanel(Panel):
    """
    The UI element enabling the user to access lists of tasks.
    """

    _EVENT_STEAM = EventStream()

    _TITLE = "Tasks"

    _GRID_SIZE = 75
    _SCOLLABLE_HEIGHT = 70  # Relative to _GRID_SIZE

    _BUILD_BUTTON_BG = "#1da334"
    _BUILD_BUTTON_FG = "#e3e3e3"
    _BUILD_BUTTON_TEXT = "+ New Task"

    def __init__(self, parent):
        super().__init__(parent)
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._tasks = Registrar()
        self._scrollable = self._init_scrollable_frame()
        self._init_build_button()
        self._subscribe_to_events()

    def _init_scrollable_frame(self):
        scrollable = guiutils.init_grid_widget(
            widgets.ScrollableFrame,
            self._frame,
            w=self._GRID_SIZE,
            h=self._SCOLLABLE_HEIGHT,
            propagate=True
        )
        return scrollable

    def _init_build_button(self):
        button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._SCOLLABLE_HEIGHT,
            w=self._GRID_SIZE,
            h=self._GRID_SIZE - self._SCOLLABLE_HEIGHT,
            bg=self._BUILD_BUTTON_BG,
            fg=self._BUILD_BUTTON_FG,
            text=self._BUILD_BUTTON_TEXT,
            command=self._new_task
        )
        return button

    def _subscribe_to_events(self):
        self._EVENT_STEAM.subscribe(Events.DEL_TASK, self._tasks.deregister)

    def _new_task(self):
        title = dialog.askstring(
            "Input",
            "Task name",
            parent=self._frame
        )
        widget = widgets.TaskWidget(
            self._scrollable.frame, 
            title, 
            subtitle="Subtitle!"
        )
        self._tasks.register(widget)
        self._render_tasks()

    def _render_tasks(self):
        for task in self._tasks:
            task.pack(fill=tk.X, pady=2, padx=5)


class TopicPanel(Panel):
    """
    The UI element enabling the user to create and select task topics.
    """

    _TITLE = "Topics"

    def __init__(self, parent):
        super().__init__(parent)
        self._topics = {}

    def _add_topic(self, name, color):
        self._topics[name] = color

    def _remove_topic(self, name):
        del self._topics[name]
