
from src.gui.abstracts import Panel


class BluePanel(Panel):

    @classmethod
    def title(cls):
        return "Blue :/"

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="blue")
