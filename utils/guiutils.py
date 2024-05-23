from PIL import Image, ImageTk
import tkinter as tk


GRID_CONF_ERR_MSG = "Cannot configure object of class {} as a grid widget"
INIT_GRID_WIDGET_ERR_MSG = "Cannot instantiate grid widget; check 'widget_cls' argument?"


def configure_grid(widget, width, height):
    """
    Configures widget to maintain a grid of the given size.
    """
    try:
        for x in range(width):
            widget.rowconfigure(index=x, weight=1)
        for y in range(height):
            widget.columnconfigure(index=y, weight=1)

    except AttributeError:
        msg = GRID_CONF_ERR_MSG.format(type(widget).__name__)
        raise TypeError(msg)


def init_grid_widget(widget_cls, parent, *args, x=0, y=0, w=0, h=0, padx=0, pady=0, sticky=tk.NSEW, **kwargs):
    """
    Creates a widget_cls object and grids it to its parent at the given coordinates.
    """
    try:
        widget = widget_cls(parent, *args, **kwargs)
        widget.grid(
            row=y,
            column=x,
            rowspan=h,
            columnspan=w,
            sticky=sticky,
            padx=padx,
            pady=pady
        )
        return widget

    except TypeError:
        raise TypeError(INIT_GRID_WIDGET_ERR_MSG)


def build_icon(path, width, height):
    """
    Produces a PhotoImage object using the given image file; suitable for use as an icon within widgets.
    """
    image = Image.open(path).resize((width, height))
    return ImageTk.PhotoImage(image)
