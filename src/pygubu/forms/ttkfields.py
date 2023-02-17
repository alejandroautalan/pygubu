import tkinter as tk
import tkinter.ttk as ttk
import pygubu.forms.validators as validators
from .exceptions import ValidationError
from .forms import BaseFormMixin
from .fields import Field, FieldInfoDisplay


class Form(BaseFormMixin, ttk.Frame):
    ...


class TkVariableBasedField(Field):
    tkvar_pname = "textvariable"
    tkvar_class = tk.StringVar

    def __init__(self, *args, **kw):
        user_var = kw.get(self.tkvar_pname, None)
        if user_var is None:
            self._data_var = self.tkvar_class()
            kw[self.tkvar_pname] = self._data_var
        elif isinstance(user_var, self.tkvar_class):
            self._data_var = user_var
        else:
            raise ValueError("Incorrect type for data variable")

        super().__init__(*args, **kw)

    @property
    def disabled(self):
        return "disabled" == self.cget("state")

    @property
    def data(self):
        return self._data_var.get()

    @data.setter
    def data(self, value):
        self._data_var.set(value)


class LabelField(TkVariableBasedField, ttk.Label):
    def __init__(self, *args, **kw):
        kw["required"] = False
        super().__init__(*args, **kw)

    def mark_invalid(self):
        pass

    def clear_invalid(self):
        pass


class CharField(TkVariableBasedField, ttk.Entry):
    def __init__(
        self,
        *args,
        max_length=None,
        min_length=None,
        strip=True,
        empty_value="",
        **kw,
    ):

        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        self.empty_value = empty_value

        kw["validate"] = kw.get("validate", "focusout")
        kw["validatecommand"] = self._self_validate
        super().__init__(*args, **kw)

        if min_length is not None:
            self.validators.append(
                validators.MinLengthValidator(int(min_length))
            )
        if max_length is not None:
            self.validators.append(
                validators.MaxLengthValidator(int(max_length))
            )

    def _self_validate(self):
        try:
            self.clean(self.data)
            return True
        except ValidationError:
            return False

    def mark_invalid(self):
        ttk.Entry.validate(self)

    def clear_invalid(self):
        ttk.Entry.validate(self)


class LabelFieldInfo(FieldInfoDisplay, ttk.Label):
    """Used to display help and errors messages for the associated form field."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._is_hidden = None
        self._layout = None
        self._layout_info = None

    def _hide(self):
        if self._is_hidden is None:
            self._layout = m = self.winfo_manager()
            if m == "pack":
                self._layout_info = self.pack_info()
                self._layout_info.pop("in", None)
                parent = self.nametowidget(self.winfo_parent())
                wlist = parent.pack_slaves()
                total = len(wlist)
                self_index = wlist.index(self)
                print("Iam in position:", self_index)
                if total > 1:
                    if self_index == 0:
                        self._layout_info["before"] = wlist[1]
                    else:
                        self._layout_info["after"] = wlist[self_index - 1]

            elif m == "place":
                self._layout_info = info = self.place_info()
                info.pop("in", None)
                # FIXME: ttkbootstrap issue with localization ??
                for key in ("relx", "rely", "relwidth", "relheight"):
                    info[key] = str(info[key]).replace(",", ".")
                print("saving place info:", self._layout_info)
            self._is_hidden = False

        if self._is_hidden is False:
            if self._layout == "pack":
                self.pack_forget()
            elif self._layout == "grid":
                self.grid_remove()
            elif self._layout == "place":
                self.place_forget()
            self._is_hidden = True

    def _show(self):
        if self._is_hidden:
            layout = self._layout
            if layout == "pack":
                self.pack(**self._layout_info)
            elif layout == "grid":
                self.grid()
            elif layout == "place":
                self.place(**self._layout_info)
            self._is_hidden = False

    def show_error(self, error):
        self._show()
        self.configure(text=error.message)

    def clear(self):
        self.configure(text="")
        self._hide()
