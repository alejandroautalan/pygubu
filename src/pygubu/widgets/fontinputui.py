#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


#
# Base class definition
#
class FontInputUI(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.wfamily = ttk.Combobox(self, name="wfamily")
        self.family_var = tk.StringVar()
        self.wfamily.configure(textvariable=self.family_var)
        self.wfamily.pack(expand=False, fill="x", side="top")
        self.wfamily.bind(
            "<<ComboboxSelected>>", self.call_process_form, add=""
        )
        self.wfamily.bind("<FocusOut>", self.call_process_form, add="")
        self.wfamily.bind("<KeyPress>", self.on_keypress, add="")
        frame3 = ttk.Frame(self)
        frame3.configure(height=200, padding="0 1p 0 0", width=200)
        self.wsize = ttk.Spinbox(frame3, name="wsize")
        self.size_var = tk.StringVar()
        self.wsize.configure(
            from_=2, textvariable=self.size_var, to=900, validate="key", width=4
        )
        self.wsize.grid(column=0, row=0, sticky="ew")
        _validatecmd = (self.wsize.register(self.on_validate_size), "%P")
        self.wsize.configure(validatecommand=_validatecmd)
        self.wsize.bind("<<Decrement>>", self.call_process_form, add="")
        self.wsize.bind("<<Increment>>", self.call_process_form, add="")
        self.wsize.bind("<KeyPress>", self.on_keypress, add="")
        self.wweight = ttk.Checkbutton(frame3, name="wweight")
        self.w_var = tk.BooleanVar()
        self.wweight.configure(
            compound="center",
            style="weight.FontInput.Toolbutton",
            variable=self.w_var,
            width=-1,
        )
        self.wweight.grid(column=1, row=0)
        self.wweight.configure(command=self.on_modifier_clicked)
        self.wslant = ttk.Checkbutton(frame3, name="wslant")
        self.s_var = tk.BooleanVar()
        self.wslant.configure(
            compound="center",
            style="slant.FontInput.Toolbutton",
            variable=self.s_var,
            width=-1,
        )
        self.wslant.grid(column=2, row=0)
        self.wslant.configure(command=self.on_modifier_clicked)
        self.wunderline = ttk.Checkbutton(frame3, name="wunderline")
        self.u_var = tk.BooleanVar()
        self.wunderline.configure(
            compound="center",
            style="underline.FontInput.Toolbutton",
            variable=self.u_var,
            width=-1,
        )
        self.wunderline.grid(column=3, row=0)
        self.wunderline.configure(command=self.on_modifier_clicked)
        self.woverstrike = ttk.Checkbutton(frame3, name="woverstrike")
        self.o_var = tk.BooleanVar()
        self.woverstrike.configure(
            compound="center",
            style="overstrike.FontInput.Toolbutton",
            variable=self.o_var,
            width=-1,
        )
        self.woverstrike.grid(column=4, row=0)
        self.woverstrike.configure(command=self.on_modifier_clicked)
        frame3.pack(expand=False, fill="x", side="top")
        frame3.columnconfigure(0, weight=1)
        frame3.columnconfigure(1, pad="6p", uniform="b")
        frame3.columnconfigure(2, uniform="b")
        frame3.columnconfigure(3, uniform="b")
        frame3.columnconfigure(4, uniform="b")
        self.configure(height=25, width=100)
        self.pack(expand=True, fill="x", side="top")

    def call_process_form(self, event=None):
        pass

    def on_keypress(self, event=None):
        pass

    def on_validate_size(self, p_entry_value):
        pass

    def on_modifier_clicked(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    widget = FontInputUI(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
