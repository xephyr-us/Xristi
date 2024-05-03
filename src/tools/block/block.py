
from src.abstracts import Panel


class GreenPanel(Panel):

    @classmethod
    def title(cls):
        return "Green :}"

    def __init__(self, parent):
        super().__init__(parent)
        self._frame.configure(bg="lime")
