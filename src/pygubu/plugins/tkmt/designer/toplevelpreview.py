import sys
import os
import json
import tkinter as tk
import TKinterModernThemes as tkmt
from pygubu.plugins.tkmt.widgets import ThemedTKinterFrameBO
from pygubu.api.v1 import register_builder


class ThemedTKinterFrameTLPreview(tkmt.ThemedTKinterFrame):
    def __init__(
        self,
        title: str,
        theme: str = "",
        mode: str = "",
        usecommandlineargs=True,
        useconfigfile=True,
    ):

        self.root: tk.Tk = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.handleExit)
        self.root.title(title)

        # region Set Theme
        if usecommandlineargs:
            args = sys.argv
            if len(args) == 3:
                theme = args[1]
                mode = args[2]

        if useconfigfile:
            try:
                with open("themeconfig.json") as f:
                    themeconfig = json.load(f)
                    if "theme" in themeconfig:
                        theme = themeconfig["theme"]
                    if "mode" in themeconfig:
                        mode = themeconfig["mode"]
            except (FileNotFoundError, json.JSONDecodeError):
                pass  # no config file was specified

        if theme == "":
            theme = "park"

        if mode == "":
            mode = "dark"

        try:
            path = os.path.abspath(
                tkmt.__file__
                + "/../themes/"
                + theme.lower()
                + "/"
                + theme.lower()
                + ".tcl"
            )
            self.root.tk.call("source", path)
        except tk.TclError:
            pass  # theme already loaded...
        self.root.tk.call("set_theme", mode.lower())

        self.theme = theme.lower()
        self.mode = mode.lower()
        # endregion

        super(tkmt.ThemedTKinterFrame, self).__init__(self.root, "Master Frame")

    def handleExit(self):
        self.root.withdraw()

    def destroy(self):
        self.root.destroy()


class ThemedTKinterFrameTLPreviewBO(ThemedTKinterFrameBO):
    class_ = ThemedTKinterFrameTLPreview


register_builder(
    "tkmt.ThemedTKinterFrameTLPreview",
    ThemedTKinterFrameTLPreviewBO,
    "ThemedTKinterFrameTLPreview",
    ("ttk",),
    public=False,
)


if __name__ == "__main__":
    test = ThemedTKinterFrameTLPreview("Preview Test")
    test.run()
