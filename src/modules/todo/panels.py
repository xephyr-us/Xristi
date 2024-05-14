
import tkinter as tk

from src.abstracts import Panel
from utils import guiutils

from src.modules.todo.widgets import TaskWidget
from src.modules.todo.structs import Registrar


class TaskPanel(Panel):

    _TITLE = "Tasks"

    _GRID_SIZE = 75
    _TASK_FRAME_HEIGHT = 70

    _BUILD_BUTTON_BG = "#1da334"
    _BUILD_BUTTON_FG = "#e3e3e3"
    _BUILD_BUTTON_TEXT = "+New Task"

    def __init__(self, parent):
        super().__init__(parent)
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._task_frame = self._init_task_frame()
        self._init_build_button()
        self._tasks = Registrar("Hello!", "again", "my old", "friend :}")
        self._render_tasks()

    def _init_task_frame(self):
        frame = guiutils.init_grid_widget(
            tk.Frame,
            self._frame,
            w=self._GRID_SIZE,
            h=self._TASK_FRAME_HEIGHT
        )
        return frame

    def _init_build_button(self):
        button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._TASK_FRAME_HEIGHT,
            w=self._GRID_SIZE,
            h=self._GRID_SIZE - self._TASK_FRAME_HEIGHT,
            bg=self._BUILD_BUTTON_BG,
            fg=self._BUILD_BUTTON_FG,
            text=self._BUILD_BUTTON_TEXT,
            command=lambda: print("Hello!")
        )
        return button

    def _add_task(self, name):
        self._tasks.register(name)

    def _remove_task(self, name):
        self._tasks.deregister(name)

    def _render_tasks(self):
        for task in self._tasks:
            widget = TaskWidget(self._task_frame, task)
            widget.pack(fill=tk.X, pady=2, padx=5)


class TopicPanel(Panel):

    _TITLE = "Topics"

    def __init__(self, parent):
        super().__init__(parent)
        self._topics = {}

    def _add_topic(self, name, color):
        self._topics[name] = color

    def _remove_topic(self, name):
        del self._topic[name]
