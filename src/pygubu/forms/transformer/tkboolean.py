import tkinter as tk
from . import DataTransformer


class BoolTransformer(DataTransformer):
    def transform(self, value):
        tval = False
        try:
            tval = tk.getboolean(value)
        except (ValueError, tk.TclError):
            pass
        return tval

    def reversetransform(self, value):
        return self.transform(value)
