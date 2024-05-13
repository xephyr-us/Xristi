
import tkinter as tk

from ..abstracts import WidgetWrapper


class LabeledWidget(WidgetWrapper):

    def __init__(self, widget_cls, parent, label, *args, **kwargs):
        super().__init__(tk.LabelFrame, parent)
        self._wrapped.configure(text=label)
        self._widget = widget_cls(self._wrapped, *args, **kwargs)
        self._widget.pack(fill=tk.BOTH, expand=True)

    @property
    def widget(self):
        return self._widget

