
from src.gui.mixins import Panel


class RedPanel(Panel):

    @classmethod
    def title(cls):
        return "Red :3"

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="red")
