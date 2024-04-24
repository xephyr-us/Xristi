import tkinter as tk


GRID_CONF_ERR_MSG = "Cannot configure object of class {} as a grid widget"
INIT_GRID_WIDGET_ERR = "Cannot instantiate grid widget; check 'widget_cls' argument?"


def configure_grid(widget, width, height):
    try:
        for x in range(width):
            widget.rowconfigure(index=x, weight=1)
        for y in range(height):
            widget.columnconfigure(y, weight=1)

    except AttributeError:
        msg = GRID_CONF_ERR_MSG.format(type(widget).__name__)
        raise TypeError(msg)


def init_grid_widget(widget_cls, parent, x, y, w, h, padx=0, pady=0):
    try:
        widget = widget_cls(parent)
        widget.grid(
            row=y,
            column=x,
            rowspan=h,
            columnspan=w,
            sticky=tk.NSEW,
            padx=padx,
            pady=pady
        )
        return widget

    except TypeError:
        raise TypeError(INIT_GRID_WIDGET_ERR)


def init_labelled_grid_widget(widget_cls, parent, label, x, y, w, h, padx=0, pady=0):
    frame = init_grid_widget(
        tk.LabelFrame,
        parent,
        x=x,
        y=y,
        w=w,
        h=h,
        padx=padx,
        pady=pady
    )
    frame.configure(text=label)
    widget = widget_cls(frame)
    widget.pack(fill=tk.BOTH, expand=True)
    return widget
