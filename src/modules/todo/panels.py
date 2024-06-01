
from tkinter import simpledialog as dialog
from tkinter import messagebox as message
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

    _NAME_DIALOG_TITLE = "Name"
    _NAME_DIALOG_PROMPT = "What's this task's name?"

    _TOPIC_DIALOG_TITLE = "Topic (Optional)"
    _TOPIC_DIALOG_PROMPT = "What topic does this task fall under?"

    _INV_TOPIC_DIALOG_PROMPT = f"No such topic! {_TOPIC_DIALOG_PROMPT}"

    def __init__(self, parent):
        super().__init__(parent)
        guiutils.configure_grid(
            self._frame,
            self._GRID_SIZE,
            self._GRID_SIZE
        )
        self._incomplete_tasks = Registrar()
        self._complete_tasks = []
        self._topic_colors = {}
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
        # New task button
        guiutils.init_grid_widget(
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

    def _subscribe_to_events(self):
        self._EVENT_STEAM.subscribe(Events.DEL_TASK, self._delete_task)
        self._EVENT_STEAM.subscribe(Events.COMPLETE_TASK, self._complete_task)
        self._EVENT_STEAM.subscribe(Events.SET_TASK_TOPICS, self._set_topics)
        self._EVENT_STEAM.subscribe(Events.SELECT_TASK_TOPIC, self._render_incomplete_tasks)
        self._EVENT_STEAM.subscribe(Events.SELECT_TASKS_COMPLETED, self._render_complete_tasks)

    def _set_topics(self, new_topics):
        self._topic_colors = new_topics

    def _new_task(self):
        name = self._prompt_task_name()
        topic = self._prompt_task_topic()
        topic_color = self._get_topic_color(topic)
        widget = widgets.TaskWidget(
            self._scrollable.frame, 
            name, 
            subtitle=topic,
            subtitle_color=topic_color
        )
        if topic is None:
            self._incomplete_tasks.register(widget)
        else:
            self._incomplete_tasks.register(widget, topic)
        self._render_incomplete_tasks()

    def _delete_task(self, task):
        self._incomplete_tasks.deregister(task)
        if task in self._complete_tasks:
            self._complete_tasks.remove(task)

    def _complete_task(self, task):
        self._incomplete_tasks.deregister(task)
        self._complete_tasks.append(task)
        self._render_incomplete_tasks()

    def _render_incomplete_tasks(self, topic=None):
        self._clear_rendered_tasks()
        tasks = self._incomplete_tasks if topic is None else self._incomplete_tasks.collect(topic)
        for task in tasks:
            task.pack(fill=tk.X, pady=2, padx=5)

    def _render_complete_tasks(self):
        self._clear_rendered_tasks()
        for task in self._complete_tasks:
            task.pack(fill=tk.X, pady=2, padx=5)

    def _clear_rendered_tasks(self):
        for child in self._scrollable.frame.winfo_children():
            child.pack_forget()

    def _prompt_task_name(self):
        return dialog.askstring(
            self._NAME_DIALOG_TITLE,
            self._NAME_DIALOG_PROMPT,
            parent=self._frame
        )

    def _prompt_task_topic(self):
        topic = dialog.askstring(
            self._TOPIC_DIALOG_TITLE,
            self._TOPIC_DIALOG_PROMPT,
            parent=self._frame
        )
        if topic == "":
            return None
        while topic not in self._topic_colors.keys():
            topic = dialog.askstring(
                self._TOPIC_DIALOG_TITLE,
                self._INV_TOPIC_DIALOG_PROMPT,
                parent=self._frame
            )
        return topic
    
    def _get_topic_color(self, topic):
        if topic is None or topic not in self._topic_colors.keys():
            return None
        return self._topic_colors[topic]


class TopicPanel(Panel):
    """
    The UI element enabling the user to create and select task topics.
    """

    _EVENT_STREAM = EventStream()

    _TITLE = "Topics"

    _GRID_SIZE = 60

    # Relative to _GRID_SIZE
    _SCROLLABLE_HEIGHT = 58
    _BUTTON_WIDTH = 20

    _NEW_BUTTON_BG = "#1da334"
    _NEW_BUTTON_FG = "#e3e3e3"
    _NEW_BUTTON_TEXT = "+ New Topic"

    _ALL_BUTTON_BG = "#173f80"
    _ALL_BUTTON_FG = "#e3e3e3"
    _ALL_BUTTON_TEXT = "All Tasks"

    _COMPLETED_BUTTON_BG = "#801717"
    _COMPLETED_BUTTON_FG = "#e3e3e3"
    _COMPLETED_BUTTON_TEXT = "Finished"

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
        self._init_buttons()
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

    def _init_buttons(self):
        # New topic button
        guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            y=self._SCROLLABLE_HEIGHT,
            w=self._BUTTON_WIDTH,
            h=self._GRID_SIZE - self._SCROLLABLE_HEIGHT,
            bg=self._NEW_BUTTON_BG,
            fg=self._NEW_BUTTON_FG,
            text=self._NEW_BUTTON_TEXT,
            command=self._add_topic
        )

        # All tasks button
        guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            x=self._BUTTON_WIDTH,
            y=self._SCROLLABLE_HEIGHT,
            w=self._BUTTON_WIDTH,
            h=self._GRID_SIZE - self._SCROLLABLE_HEIGHT,
            bg=self._ALL_BUTTON_BG,
            fg=self._ALL_BUTTON_FG,
            text=self._ALL_BUTTON_TEXT,
            command=self._select_all_tasks
        )

        # Completed tasks button
        guiutils.init_grid_widget(
            tk.Button,
            self._frame,
            x=self._BUTTON_WIDTH * 2,
            y=self._SCROLLABLE_HEIGHT,
            w=self._BUTTON_WIDTH,
            h=self._GRID_SIZE - self._SCROLLABLE_HEIGHT,
            bg=self._COMPLETED_BUTTON_BG,
            fg=self._COMPLETED_BUTTON_FG,
            text=self._COMPLETED_BUTTON_TEXT,
            command=self._select_completed_tasks
        )

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
        button.bind("<Button-1>", lambda _, topic=topic: self._select_topic_tasks(topic))
        button.bind("<Button-3>", lambda _, topic=topic: self._remove_topic(topic))
        return button

    def _render_topic_buttons(self):
        for button in self._topic_buttons.values():
            button.pack(fill=tk.X)

    def _select_topic_tasks(self, topic):
        self._EVENT_STREAM.publish(Events.SELECT_TASK_TOPIC, topic)

    def _select_all_tasks(self):
        self._EVENT_STREAM.publish(Events.SELECT_TASK_TOPIC, None)

    def _select_completed_tasks(self):
        self._EVENT_STREAM.publish(Events.SELECT_TASKS_COMPLETED)
