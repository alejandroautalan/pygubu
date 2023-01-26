import functools
import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC, abstractmethod


class InplaceEditor(ABC):
    event_value_changed = "<<InplaceEditor:ValueChanged>>"

    def _notify_change(self) -> None:
        self.widget.event_generate(self.event_value_changed)

    def focus_set(self) -> None:
        self.widget.focus_set()

    @property
    @abstractmethod
    def widget(self) -> tk.Widget:
        ...

    @property
    @abstractmethod
    def value(self):
        ...

    @abstractmethod
    def edit(self, value) -> None:
        ...


class _VariableBasedEditor(InplaceEditor):
    @abstractmethod
    def _create_widget(self, master, **kw) -> tk.Widget:
        ...

    def __init__(self, master, **kw):
        self._var_blocked = False
        self._variable = None
        if kw is None:
            kw = {}
        if "textvariable" in kw:
            self._variable = kw["textvariable"]
        else:
            self._variable = tk.StringVar()
            kw["textvariable"] = self._variable
        self._widget = self._create_widget(master, **kw)

        def on_var_write(var, index, mode):
            if not self._var_blocked:
                self._notify_change()

        self._variable.trace_add("write", on_var_write)

    @property
    def widget(self):
        return self._widget

    @property
    def value(self):
        return self._variable.get()

    def edit(self, value):
        self._var_blocked = True
        self._variable.set(value)
        self._var_blocked = False


class _EntryEditor(_VariableBasedEditor):
    def _create_widget(self, master, **kw) -> tk.Widget:
        return ttk.Entry(master, **kw)


class _CheckbuttonEditor(_VariableBasedEditor):
    def _create_widget(self, master, **kw) -> tk.Widget:
        return ttk.Checkbutton(master, **kw)


class _ComboboxEditor(_VariableBasedEditor):
    def _create_widget(self, master, **kw) -> tk.Widget:
        return ttk.Combobox(master, **kw)


class _SpinboxEditor(_VariableBasedEditor):
    def _create_widget(self, master, **kw) -> tk.Widget:
        return ttk.Spinbox(master, **kw)


class _CustomEditor(_VariableBasedEditor):
    def __init__(self, widget, **kw):
        self._widget = widget
        super().__init__(widget, **kw)

    def _create_widget(self, master, **kw) -> tk.Widget:
        return self._widget


class EditableTreeview(ttk.Treeview):
    """A simple editable treeview

    It uses the following events from Treeview:
        <<TreviewSelect>>
        <4>
        <5>
        <KeyRelease>
        <Home>
        <End>
        <Configure>
        <Button-1>
        <ButtonRelease-1>
        <Motion>
    If you need them use add=True when calling bind method.

    It Generates three virtual events:
        <<TreeviewInplaceEdit>>
        <<TreeviewCellEdited>>
        <<TreeviewEditorsUnfocused>>

    <<TreeviewInplaceEdit>> is emitted and used to configure cell editors.
    <<TreeviewCellEdited>> is emitted after a cell was changed.
    <<TreeviewEditorsUnfocused>> is emitted when user clicks in treeview
    white area where no rows are rendered.

    You can know wich cell is being configured or edited, using:
        get_event_info()

    To quickly get data from tree columns you can use:
        get_value(col, item)

    """

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self._curfocus = None
        self._editors = {}
        self._editors_show = {}
        self._header_clicked = False
        self._header_dragged = False
        self._last_column_clicked = "#0"
        self._update_callback_id = None

        self.bind("<<TreeviewSelect>>", self.__check_focus)
        # Wheel events?
        self.bind("<4>", self._schedule_update)
        self.bind("<5>", self._schedule_update)
        self.bind("<KeyRelease>", self.__check_focus)
        self.bind("<Home>", functools.partial(self.__on_key_press, "Home"))
        self.bind("<End>", functools.partial(self.__on_key_press, "End"))
        self.bind("<Button-1>", self.__on_button1)
        self.bind("<ButtonRelease-1>", self.__on_button1_release)
        self.bind("<Motion>", self.__on_mouse_motion)
        self.bind("<Configure>", self._schedule_update)

    def _schedule_update(self, event=None):
        if self._update_callback_id is None:
            self._update_callback_id = self.after_idle(self.__updateWnds)

    def __on_button1(self, event):
        r = self.identify_region(event.x, event.y)
        if r in ("separator", "header"):
            self._header_clicked = True
        elif r in ("tree", "cell"):
            if not self._editors_show:
                self._schedule_update()
        elif r == "nothing":
            if self._editors_show:
                self.__clear_inplace_widgets()
                self._curfocus = None
                self.event_generate("<<TreeviewEditorsUnfocused>>")
        self._last_column_clicked = self.identify_column(event.x)

    def __on_mouse_motion(self, event):
        if self._header_clicked:
            self._header_dragged = True

    def __on_button1_release(self, event):
        if self._header_dragged:
            self._schedule_update(event)
        self._header_clicked = False
        self._header_dragged = False

    def __on_key_press(self, key, event):
        if key == "Home":
            self.selection_set("")
            self.focus(self.get_children()[0])
        if key == "End":
            self.selection_set("")
            self.focus(self.get_children()[-1])

    def delete(self, *items):
        self._schedule_update()
        ttk.Treeview.delete(self, *items)

    def yview(self, *args):
        """Update inplace widgets position when doing vertical scroll"""
        self._schedule_update()
        ttk.Treeview.yview(self, *args)

    def yview_scroll(self, number, what):
        self._schedule_update()
        ttk.Treeview.yview_scroll(self, number, what)

    def yview_moveto(self, fraction):
        self._schedule_update()
        ttk.Treeview.yview_moveto(self, fraction)

    def xview(self, *args):
        """Update inplace widgets position when doing horizontal scroll"""
        self._schedule_update()
        ttk.Treeview.xview(self, *args)

    def xview_scroll(self, number, what):
        self._schedule_update()
        ttk.Treeview.xview_scroll(self, number, what)

    def xview_moveto(self, fraction):
        self._schedule_update()
        ttk.Treeview.xview_moveto(self, fraction)

    def __check_focus(self, event):
        """Checks if the focus has changed"""
        changed = False
        if not self._curfocus:
            changed = True
        elif self._curfocus != self.focus():
            self.__clear_inplace_widgets()
            changed = True
        newfocus = self.focus()
        if changed:
            if newfocus:
                # print('Focus changed to:', newfocus)
                self._curfocus = newfocus
                self.__focus(newfocus)
            self.__updateWnds()

    def __focus(self, item):
        """Called when focus item has changed"""
        cols = self.__get_display_columns()
        for col in cols:
            self.__event_info = (col, item)
            self.event_generate("<<TreeviewInplaceEdit>>")

    def __updateWnds(self, event=None):
        if not self._curfocus:
            return
        item = self._curfocus
        item_exists = self.exists(item)
        cols = self.__get_display_columns()
        col_diff = 0 if "#0" in cols else -1
        last_column_index = int(self._last_column_clicked[1:]) + col_diff
        for index, col in enumerate(cols):
            if col in self._editors:
                editor = self._editors[col]
                bbox = "" if not item_exists else self.bbox(item, column=col)
                if bbox == "":
                    editor.widget.place_forget()
                elif col in self._editors_show:
                    editor.widget.place(
                        x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3]
                    )
                    # try to focus the widget in the column clicked
                    if last_column_index == index:
                        editor.focus_set()
        self._update_callback_id = None

    def __clear_inplace_widgets(self):
        """Remove all inplace edit widgets."""
        for col, editor in self._editors.items():
            editor.widget.place_forget()
        self._editors_show.clear()

    def __get_display_columns(self):
        cols = self.cget("displaycolumns")
        show = (str(s) for s in self.cget("show"))
        if "#all" in cols or "tree" in show:
            cols = ("#0",) + self.cget("columns")
        return cols

    def get_event_info(self):
        return self.__event_info

    def get_value(self, col, item):
        """Return data value of tree item at the specified column index."""
        return self.__get_value(col, item)

    def __get_value(self, col, item):
        if col == "#0":
            return self.item(item, "text")
        else:
            return self.set(item, col)

    def __set_value(self, col, item, value):
        if col == "#0":
            self.item(item, text=value)
        else:
            self.set(item, col, value)
        self.__event_info = (col, item)
        self.event_generate("<<TreeviewCellEdited>>")

    def __update_value(self, col, item):
        if not self.exists(item):
            return
        value = self.__get_value(col, item)
        newvalue = self._editors[col].value
        if value != newvalue:
            self.__set_value(col, item, newvalue)

    def _setup_editor(self, col, item, editor):
        editor.edit(self.__get_value(col, item))

        def on_value_change(event):
            self.__update_value(col, item)

        editor.widget.bind(InplaceEditor.event_value_changed, on_value_change)
        self._editors_show[col] = True

    def inplace_entry(self, col, item):
        if col not in self._editors:
            self._editors[col] = _EntryEditor(self)
        self._setup_editor(col, item, self._editors[col])

    def inplace_checkbutton(self, col, item, onvalue="True", offvalue="False"):
        if col not in self._editors:
            svar = tk.StringVar()
            self._editors[col] = _CheckbuttonEditor(
                self,
                textvariable=svar,
                variable=svar,
                onvalue=onvalue,
                offvalue=offvalue,
            )
        self._setup_editor(col, item, self._editors[col])

    def inplace_combobox(
        self, col, item, values, readonly=True, update_values=False
    ):
        if col not in self._editors:
            state = "readonly" if readonly else "normal"
            self._editors[col] = _ComboboxEditor(
                self, values=values, state=state
            )
        self._setup_editor(col, item, self._editors[col])
        if update_values:
            self._editors[col].widget.configure(values=values)

    def inplace_spinbox(self, col, item, min, max, step):
        if col not in self._editors:
            self._editors[col] = _SpinboxEditor(
                self, from_=min, to=max, increment=step
            )
        self._setup_editor(col, item, self._editors[col])

    def inplace_custom(self, col, item, widget, stringvar=None):
        if col not in self._editors:
            if stringvar is None:
                stringvar = tk.StringVar()
            self._editors[col] = _CustomEditor(widget, textvariable=stringvar)
        self._setup_editor(col, item, self._editors[col])

    def inplace_editor(self, col, item, editor: InplaceEditor):
        if col not in self._editors:
            self._editors[col] = editor
        self._setup_editor(col, item, self._editors[col])
