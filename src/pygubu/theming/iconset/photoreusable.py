import tkinter as tk


class ReusableImageMixin:
    """Mixin class to keep image names in tcl."""

    def __init__(self, *args, **kw):
        self._tcl_keep = False
        super().__init__(*args, **kw)

    def tcl_keep(self):
        self._tcl_keep = True

    def __del__(self):
        if not self._tcl_keep:
            super().__del__()


class PhotoImageReusable(ReusableImageMixin, tk.PhotoImage):
    """PhotoImage class to keep image names in tcl."""

    ...
