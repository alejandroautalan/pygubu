import tkinter as tk
import tkinter.ttk as ttk


class EntryWPlaceholder(ttk.Entry):
    _PHKEY = "placeholder"

    def __init__(self, master=None, **kw):
        self.placeholder = kw.pop(self._PHKEY, "")
        super().__init__(master, **kw)

        self.bind("<FocusIn>", self._on_focusin)
        self.bind("<FocusOut>", self._on_focusout)

        if "textvariable" in kw:
            var = kw["textvariable"]
            var.trace_add("write", self._trace_var)
        self._put_placeholder()

    def _trace_var(self, var, *args):
        print(f"tracing {var}", self.__get())
        if self.focus_displayof() is not self:
            print("putting placeholder after var trace")
            self._put_placeholder(self.__get())

    def _put_placeholder(self):
        print("on put_placeholder", self.__get(), not self.__get())
        if not self.__get():
            print("inserting placeholder")
            self.insert(0, self.placeholder)

    def _on_focusin(self, event):
        print("on_focusin")
        if self.__get() == self.placeholder:
            print("deleting placeholder")
            self.delete("0", "end")

    def _on_focusout(self, event):
        self._put_placeholder()

    def __get(self):
        return super().get()

    def get(self):
        value = super().get()
        if value and (value == self.placeholder):
            value = ""
        return value

    def configure(self, cnf=None, **kw):
        key = self._PHKEY
        if cnf:
            if cnf == key:
                return (key, self.cget(key))
            return super().configure(cnf, **kw)
        if key in kw:
            self.placeholder = kw.pop(key)
            self._put_placeholder()
        return super().configure(cnf, **kw)

    config = configure

    def cget(self, key):
        if key == self._PHKEY:
            return self.placeholder
        return super().cget(key)

    __getitem__ = cget


if __name__ == "__main__":
    root = tk.Tk()
    var = tk.StringVar()
    username = EntryWPlaceholder(root, textvariable=var)
    username["placeholder"] = "--USERNAME--"

    var2 = tk.StringVar()
    password = EntryWPlaceholder(root, textvariable=var2)
    password.configure(style="MyPasswordEntry.TEntry")
    password.configure(placeholder="--PASSWORD--")

    username.pack()
    password.pack()

    def on_click():
        print(f"user: {username.get()}")
        print(f"pass: {password.get()}")

    def on_start():
        var.set("username")

    btn = ttk.Button(root, text="Test", takefocus=True, command=on_click)
    btn.pack()
    root.after(800, on_start)
    root.mainloop()
