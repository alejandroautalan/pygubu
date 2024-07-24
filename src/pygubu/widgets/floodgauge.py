import tkinter as tk
import tkinter.ttk as ttk
from pygubu.utils.widget import WidgetConfigureMixin


"""Floodgauge Widget

Based on ttkbootstrap Floodgauge.
"""


class FloodgaugeStyleManager:
    """Manage PygubuFloodgauge style

    Tasks:
        - register style if not defined
        - update style if theme changed
        - do nothing if style is previously defined
          (if using pygubu theming).
    """

    TKCLASS_NAME: str = "Floodgauge"
    STYLE_NAME_H: str = None
    STYLE_NAME_V: str = None
    STYLE_LAYOUT_H: list = None
    STYLE_LAYOUT_V: list = None
    STYLE_CONF: dict = None
    STYLE_INITIALIZED = False
    STYLE_MANAGED_EXTERNALLY = False
    CONFIGURED_THEMES = None

    @classmethod
    def define_layout(cls, master):
        if cls.STYLE_INITIALIZED or cls.STYLE_MANAGED_EXTERNALLY:
            return

        H_STYLE = f"Horizontal.T{cls.TKCLASS_NAME}"
        V_STYLE = f"Vertical.T{cls.TKCLASS_NAME}"

        cls.STYLE_NAME_H = H_STYLE
        cls.STYLE_NAME_V = V_STYLE

        style = ttk.Style(master)
        try:
            h_layout = style.layout(H_STYLE)
            v_layout = style.layout(V_STYLE)
            if h_layout and v_layout:
                cls.STYLE_MANAGED_EXTERNALLY = True
                cls.STYLE_LAYOUT_H = h_layout
                cls.STYLE_LAYOUT_V = v_layout
                return
        except tk.TclError:
            pass

        h_element = H_STYLE.replace(".TF", ".F")
        v_element = V_STYLE.replace(".TF", ".F")
        style.element_create(f"{h_element}.trough", "from", "clam")
        style.element_create(f"{h_element}.pbar", "from", "default")
        style.element_create(f"{v_element}.trough", "from", "clam")
        style.element_create(f"{v_element}.pbar", "from", "default")
        h_layout = [
            (
                f"{h_element}.trough",
                {
                    "children": [
                        (
                            f"{h_element}.pbar",
                            {"sticky": "ns"},
                        ),
                        (f"{cls.TKCLASS_NAME}.label", {"sticky": ""}),
                    ],
                    "sticky": "nsew",
                },
            )
        ]
        v_layout = [
            (
                f"{v_element}.trough",
                {
                    "children": [
                        (
                            f"{v_element}.pbar",
                            {"sticky": "ew"},
                        ),
                        (f"{cls.TKCLASS_NAME}.label", {"sticky": ""}),
                    ],
                    "sticky": "nsew",
                },
            )
        ]
        bg_color = style.lookup("TProgressbar", "background")
        default_conf = dict(
            background=bg_color,
            borderwidth=1,
            font="-size 14",
            thickness=50,
            pbarrelief=tk.FLAT,
            justify=tk.CENTER,
            anchor=tk.CENTER,
        )
        style.layout(H_STYLE, h_layout)
        style.configure(H_STYLE, **default_conf)
        style.layout(V_STYLE, v_layout)
        style.configure(V_STYLE, **default_conf)

        cls.CONFIGURED_THEMES = [style.theme_use()]
        cls.STYLE_LAYOUT_H = h_layout
        cls.STYLE_LAYOUT_V = v_layout
        cls.STYLE_CONF = default_conf
        cls.STYLE_INITIALIZED = True

    @classmethod
    def reconfigure_layout(cls, master):
        if cls.STYLE_MANAGED_EXTERNALLY:
            return
        theme = master.tk.eval("return $ttk::currentTheme")
        if theme not in cls.CONFIGURED_THEMES:
            s = ttk.Style(master)
            bg_color = s.lookup("TProgressbar", "background")
            conf = cls.STYLE_CONF
            conf.update(background=bg_color)
            s.configure(cls.STYLE_NAME_H, **conf)
            s.configure(cls.STYLE_NAME_V, **conf)
            cls.CONFIGURED_THEMES.append(theme)

    @classmethod
    def style_for_orient(cls, orient):
        return cls.STYLE_NAME_H if orient == "horizontal" else cls.STYLE_NAME_V

    @classmethod
    def layout_for_orient(cls, orient):
        return (
            cls.STYLE_LAYOUT_H if orient == "horizontal" else cls.STYLE_LAYOUT_V
        )


class Floodgauge(WidgetConfigureMixin, ttk.Progressbar):
    """A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `ttk.Progressbar`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.
    """

    INSTANCE_COUNT = 0
    FGSM = FloodgaugeStyleManager()

    def __init__(self, master=None, **kw):
        self.FGSM.define_layout(master)
        self._uid = self._new_uid()
        self._pmask = kw.pop("mask", None)
        self._pfont = kw.pop("font", "helvetica 10")
        self._pvariable = kw.get("variable", None)
        self._ptextvar = kw.pop("textvariable", None)
        self._traceid = None

        orient = kw.get("orient", "horizontal")
        default_style = self.FGSM.style_for_orient(orient)
        user_defined_style = kw.get(
            "style", default_style
        )  # user defined style
        value = kw.get("value", 0)

        text = kw.pop("text", "")
        if self._pvariable is None:
            self._pvariable = tk.IntVar(master, value=value)
        if self._ptextvar is None:
            self._ptextvar = tk.StringVar(master, value=text)

        kw["style"] = self._new_instance_style(
            master, orient, user_defined_style
        )
        kw["class_"] = self.FGSM.TKCLASS_NAME
        kw["value"] = value
        kw["variable"] = self._pvariable
        super().__init__(master, **kw)
        self.bind("<<ThemeChanged>>", self._on_theme_change)
        self.bind("<<Configure>>", self._on_theme_change)
        self._set_widget_text()
        if self._pmask is not None:
            self._set_mask()

    @classmethod
    def _new_uid(cls):
        cls.INSTANCE_COUNT += 1
        return f"fg{cls.INSTANCE_COUNT}"

    def _set_widget_text(self, *_):
        ttkstyle = self.cget("style")
        if self._pmask is None:
            text = self._ptextvar.get()
        else:
            value = self._pvariable.get()
            text = self._pmask.format(value)
        self.tk.call("ttk::style", "configure", ttkstyle, "-text", text)
        self.tk.call("ttk::style", "configure", ttkstyle, "-font", self._pfont)

    def _set_mask(self):
        if self._traceid is None:
            self._traceid = self._pvariable.trace_add(
                "write", self._set_widget_text
            )

    def _unset_mask(self):
        if self._traceid is not None:
            self._pvariable.trace_remove("write", self._traceid)
        self._traceid = None

    def _new_instance_style(self, master, orient: str, style: str) -> str:
        instance_style = style
        uid = f"{self._uid}."

        if not style.startswith(uid):
            instance_style = f"{uid}{style}"

        layout_exists = False
        s = ttk.Style(master)
        try:
            s.layout(instance_style)
        except tk.TclError:
            pass
        if not layout_exists:
            s.layout(instance_style, self.FGSM.layout_for_orient(orient))
        return instance_style

    def _on_theme_change(self, event=None):
        self.FGSM.reconfigure_layout(self)
        self._set_widget_text()

    def _widget_cget(self, option):
        if option == "value":
            return self._pvariable.get()
        if option == "text":
            return self._ptextvar.get()
        if option == "mask":
            return self._pmask
        if option == "font":
            return self._pfont
        if option == "textvariable":
            return self._ptextvar
        return super()._widget_cget(option)

    def _configure_get(self, option):
        if option in ("value", "text", "mask", "font", "textvariable"):
            return self._widget_cget(option)
        return super()._configure_get(option)

    def _configure_set(self, **kw):
        update_text = False
        update_style = False

        if "style" in kw or "orient" in kw:
            update_text = True
            update_style = True
        pname = "variable"
        if pname in kw:
            new_var = kw[pname]
            self._unset_mask()
            self._pvariable = new_var
            if new_var and self._pmask:
                self._set_mask()
            update_text = True
        pname = "value"
        if pname in kw:
            self._pvariable.set(kw.pop(pname))
            update_text = True
        pname = "text"
        if pname in kw:
            self._ptextvar.set(kw.pop(pname))
            update_text = True
        pname = "mask"
        if pname in kw:
            self._pmask = kw.pop(pname)
            if self._pmask:
                self._set_mask()
            update_text = True
        pname = "font"
        if pname in kw:
            self._pfont = kw.pop(pname)
            update_text = True
        pname = "textvariable"
        if pname in kw:
            self._ptextvar = kw.pop(pname)
            update_text = True
        if update_style:
            orient = kw.get("orient", self.cget("orient"))
            style = kw.get("style", self.FGSM.style_for_orient(orient))
            new_style = self._new_instance_style(self, orient, style)
            kw["style"] = new_style
        if update_text:
            self._set_widget_text()
        return super()._configure_set(**kw)


if __name__ == "__main__":
    root = tk.Tk()
    gauge = Floodgauge(root, mask="{}%")
    gauge.pack(expand=True, fill="both")
    options = ("value", "text", "mask", "font", "textvariable", "variable")
    for option in options:
        value = gauge.cget(option)
        print(f"The gauge {option} is:", value, type(value))

    scale = ttk.Scale(
        root, variable=gauge.cget("variable"), value=0, from_=0, to=100
    )
    scale.pack()

    root.mainloop()
