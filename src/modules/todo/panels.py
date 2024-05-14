
import tkinter as tk

from src.abstracts import Panel

from src.modules.todo.widgets import TaskWidget
from src.modules.todo.structs import Registrar


class TaskPanel(Panel):

    _TITLE = "Tasks"

    def __init__(self, parent):
        super().__init__(parent)
        self._tasks = {
            "Test1",
            "Test2",
            "Test3"
        }
        self._render_tasks()

    def _add_task(self, name):
        self._tasks.add(name)

    def _delete_task(self, name):
        self._tasks.remove(name)

    def _render_tasks(self):
        for task in self._tasks:
            widget = TaskWidget(self._frame, task)
            widget.pack(fill=tk.X)


class TopicPanel(Panel):

    _TITLE = "Topics"

    def __init__(self, parent):
        super().__init__(parent)
        self._topics = {}

    def _add_topic(self, name, color):
        self._topics[name] = color

    def _remove_topic(self, name):
        del self._topic[name]
