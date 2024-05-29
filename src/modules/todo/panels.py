
from tkinter import simpledialog as dialog
from tkinter import colorchooser
import tkinter as tk

from src.event_handling import EventStream, Events
from utils import guiutils, pyutils
from src.abstracts import Panel

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

    _BUTTON_BG = "#1da334"
    _BUTTON_FG = "#e3e3e3"
    _BUTTON_TEXT = "+ New Task"

    _TEXT_DIALOG_TITLE = "Text"
    _TEXT_DIALOG_PROMPT = "Task name"

    def __init__(self, parent):
        super().__init__(parent)
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._tasks = Registrar()
        self._topics = {}
        self._scrollable = self._init_scrollable_frame()
        self._init_button()
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

    def _init_button(self):
        button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._SCOLLABLE_HEIGHT,
            w=self._GRID_SIZE,
            h=self._GRID_SIZE - self._SCOLLABLE_HEIGHT,
            bg=self._BUTTON_BG,
            fg=self._BUTTON_FG,
            text=self._BUTTON_TEXT,
            command=self._new_task
        )
        return button

    def _subscribe_to_events(self):
        self._EVENT_STEAM.subscribe(Events.DEL_TASK, self._tasks.deregister)
        self._EVENT_STEAM.subscribe(Events.SET_TASK_TOPICS, self._set_topics)

    def _set_topics(self, new_topics):
        self._topics = new_topics

    def _new_task(self):
        title = dialog.askstring(
            self._TEXT_DIALOG_TITLE,
            self._TEXT_DIALOG_PROMPT,
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

    _EVENT_STREAM = EventStream()

    _TITLE = "Topics"

    _GRID_SIZE = 50
    _SCROLLABLE_HEIGHT = 49

    _BUTTON_BG = "#1da334"
    _BUTTON_FG = "#e3e3e3"
    _BUTTON_TEXT = "+ New Topic"

    _TEXT_DIALOG_TITLE = "Text"
    _TEXT_DIALOG_PROMPT = "Topic name"

    @staticmethod
    def _calc_fg(bg):
        brightness = 0
        for i in range(1, 7, 2):
            brightness += int(bg[i:i+2], base=16)
        rel_avg_brightness = (brightness / 3) / 255
        return "white" if rel_avg_brightness < 0.5 else "black"

    def __init__(self, parent):
        super().__init__(parent)
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._scrollable = self._init_scrollable_panel()
        self._button = self._init_button()
        self._topic_buttons = {}
        self._topics = {}

    def _init_scrollable_panel(self):
        scrollable = guiutils.init_grid_widget(
            widgets.ScrollableFrame,
            self._frame,
            w=self._GRID_SIZE,
            h=self._SCROLLABLE_HEIGHT
        )
        return scrollable

    def _init_button(self):
        button = guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._SCROLLABLE_HEIGHT,
            w=self._GRID_SIZE,
            h=self._GRID_SIZE - self._SCROLLABLE_HEIGHT,
            bg=self._BUTTON_BG,
            fg=self._BUTTON_FG,
            text=self._BUTTON_TEXT,
            command=self._add_topic
        )
        return button

    def _add_topic(self):
        topic = dialog.askstring(
            self._TEXT_DIALOG_TITLE,
            self._TEXT_DIALOG_PROMPT,
            parent=self._frame
        )
        color = colorchooser.askcolor(
            parent=self._frame
        )[1]
        self._topics[topic] = color
        self._EVENT_STREAM.publish(
            Events.SET_TASK_TOPICS, 
            self._topics.copy()
        )
        button = self._build_topic_button(topic, color)
        self._topic_buttons[topic] = button
        self._render_topic_buttons()

    def _remove_topic(self, topic):
        del self._topics[topic]
        button = self._topic_buttons[topic]
        button.destroy()
        del self._topic_buttons[topic]
        self._EVENT_STREAM.publish(
            Events.SET_TASK_TOPICS, 
            self._topics.copy()
        )

    def _build_topic_button(self, topic, color):
        button = tk.Button(
            self._scrollable.frame,
            text=topic,
            bg=color,
            fg=self._calc_fg(color),
        )
        button.bind("<Button-1>", lambda _, topic=topic: self._render_topic_tasks(topic))
        button.bind("<Button-3>", lambda _, topic=topic: self._remove_topic(topic))
        return button

    def _render_topic_buttons(self):
        for button in self._topic_buttons.values():
            button.pack(fill=tk.X)

    def _render_topic_tasks(self, topic):
        print(topic)
