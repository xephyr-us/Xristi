
import tkinter as tk
import os

from .mixins import Panel


class ToolPanel(Panel):

    _MODULE_DEF_FILENAME = "MANIFEST"

    @staticmethod
    def _absolute_subdirectories(path):
        assert os.path.isdir(path)
        for file in os.listdir(path):
            subpath = os.path.join(path, file)
            if os.path.isdir(subpath):
                yield os.path.abspath(subpath)

    @staticmethod
    def _is_in_directory(filename, path):
        assert os.path.isdir(path)
        return filename in os.listdir(path)

    @classmethod
    def title(cls):
        return "Tools"

    def __init__(self, parent, modules_dir):
        super().__init__(parent)
        self._buttons = self._init_buttons(modules_dir)

    def _init_buttons(self, modules):
        buttons = []
        for subdir in self._absolute_subdirectories(modules):
            if self._is_in_directory(self._MODULE_DEF_FILENAME, subdir):
                definition = os.path.join(subdir, self._MODULE_DEF_FILENAME)
        return buttons


class BlankPanel(Panel):

    @classmethod
    def title(cls):
        return "Blank"

    def __init__(self, parent):
        super().__init__(parent)

