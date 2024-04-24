import tkinter as tk


GRID_CONF_ERR_MSG = "Cannot configure object of class {} as a grid widget"
INIT_WIDGET_ERR = "Improper usage of function {}, see below error"


def configure_grid(widget, width, height):
    try:
        for x in range(width):
            widget.rowconfigure(index=x, weight=1)
        for y in range(height):
            widget.columnconfigure(y, weight=1)

    except AttributeError:
        msg = GRID_CONF_ERR_MSG.format(type(widget).__name__)
        raise AttributeError(msg)


def init_grid_widget(widget_cls, parent, x, y, w, h):
    widget = widget_cls(parent)
    widget.grid(
        row=y,
        column=x,
        rowspan=h,
        columnspan=w,
        sticky=tk.NSEW
    )
    return widget
