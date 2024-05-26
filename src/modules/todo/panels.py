
from tkinter import simpledialog as dialog
import tkinter as tk

from src.event_handling import EventStream, Events
from src.abstracts import Panel
from utils import guiutils

from src.modules.todo.widgets import TaskWidget
from src.modules.todo.structs import Registrar


class TaskPanel(Panel):
    """
    The UI element enabling the user to access lists of tasks.
    """

    _EVENT_STEAM = EventStream()

    _TITLE = "Tasks"

    _GRID_SIZE = 75
    _TASK_CANVAS_HEIGHT = 70  # Relative to _GRID_SIZE
    _SCROLLBAR_WIDTH = 1  # Relative to _GRID_SIZE

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
        self._task_canvas = self._init_task_canvas()
        self._task_frame = self._init_task_frame()
        self._scrollbar = self._init_scrollbar()
        self._init_build_button()
        self._config_scrolling()
        self._subscribe_to_events()

    def _init_task_canvas(self):
        canvas = guiutils.init_grid_widget(
            tk.Canvas,
            self._frame,
            borderwidth=0,
            w=self._GRID_SIZE - self._SCROLLBAR_WIDTH,
            h=self._TASK_CANVAS_HEIGHT,
            propagate=True
        )
        return canvas

    def _init_task_frame(self):
        frame = tk.Frame(
            self._task_canvas, 
            )
        return frame
    
    def _init_scrollbar(self):
        scrollbar = guiutils.init_grid_widget(
            tk.Scrollbar,
            self._frame,
            orient=tk.VERTICAL,
            command=self._task_canvas.yview,
            x=self._GRID_SIZE - self._SCROLLBAR_WIDTH,
            w=self._SCROLLBAR_WIDTH,
            h=self._TASK_CANVAS_HEIGHT
        )
        return scrollbar

    def _init_build_button(self):
        button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._TASK_CANVAS_HEIGHT,
            w=self._GRID_SIZE,
            h=self._GRID_SIZE - self._TASK_CANVAS_HEIGHT,
            bg=self._BUILD_BUTTON_BG,
            fg=self._BUILD_BUTTON_FG,
            text=self._BUILD_BUTTON_TEXT,
            command=self._new_task
        )
        return button
    
    def _config_scrolling(self):
        self._task_canvas.config(yscrollcommand=self._scrollbar.set)
        self._task_canvas.create_window(
            (4, 4), 
            window=self._task_frame, 
            anchor="nw"
        )

        def on_frame_config(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self._task_frame.bind("<Configure>", lambda _, canvas=self._task_canvas: on_frame_config(canvas))

    def _subscribe_to_events(self):
        self._EVENT_STEAM.subscribe(Events.DEL_TASK, self._tasks.deregister)

    def _new_task(self):
        title = dialog.askstring(
            "Input",
            "Task name",
            parent=self._frame
        )
        widget = TaskWidget(self._task_frame, title, subtitle="Subtitle!")
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
