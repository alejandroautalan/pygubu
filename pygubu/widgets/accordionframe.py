# encoding: UTF-8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
except:
    import Tkinter as tk
    import ttk

img_down = '''\
R0lGODlhEAAQAIAAAAAAAAAAACH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAEALAAAAAAQABAA
AAIXjI+py+0P4wK0WprunRo0/VgRJpXmyRQAOw==
'''

img_right = '''\
R0lGODlhEAAQAIAAAAAAAAAAACH+EUNyZWF0ZWQgd2l0aCBHSU1QACH5BAEKAAEALAAAAAAQABAA
AAIdjI+pywGtwINHTmpvy3rxnnwQh1mUI52o6rCuWgAAOw==
'''


class AccordionFrame(ttk.Frame):
    """ An accordion like widget.
    Usage:
        acframe = AccordionFrame(master)
        acframe.grid()
        g = acframe.add_group('g1', 'Group1')
        label = ttk.Label(g, text='Label on group1')
        label.grid()
    """
    IMAGES = None

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.__images = None
        self.__groups = {}
        self.columnconfigure(0, weight=1)

        if AccordionFrame.IMAGES is None:
            AccordionFrame.IMAGES = [
                tk.PhotoImage(data=img_down),
                tk.PhotoImage(data=img_right),]
        self.__images = AccordionFrame.IMAGES



    def add_group(self, gid, label=None, expanded=True):

        glabel = label
        if label is None:
            glabel = str(gid)

        #button creation
        btn = ttk.Button(self, text=glabel, style='Toolbutton',
            image=self.__images[0], compound='left')
        btn.grid(sticky=tk.EW)
        btn.dd_show = True
        btn.configure(command=lambda:self.__button_clicked(gid))

        #frame creation
        frame = ttk.Frame(self, width=100, height=100)
        frame.grid(sticky=tk.NSEW)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        if not expanded:
            self.after_idle(lambda: self.__button_clicked(gid))

        #store button, and frame
        self.__groups[gid] = (btn, frame)

        return frame


    def get_group(self, gid):
        return self.__groups[gid][1]


    def group_toogle(self, gid):
        self.__button_clicked(gid)


    def __button_clicked(self, gid):
        btn, frame = self.__groups[gid]
        if btn.dd_show == True:
            btn.dd_show = False
            btn.configure(image=self.__images[1])
            frame.grid_remove()
        else:
            btn.dd_show = True
            btn.configure(image=self.__images[0])
            frame.grid()
        self.event_generate('<<AccordionGroupToggle>>')


    def set_images(self, img_open, img_close):
        if self.__images == AccordionFrame.IMAGES:
            self.__images = [
                tk.PhotoImage(file=img_open),
                tk.PhotoImage(file=img_close),]
        else:
            self.__images[0].configure(file=img_open)
            self.__images[1].configure(file=img_close)


    @classmethod
    def set_gimages(cls, img_open, img_close):
        if cls.IMAGES is None:
            cls.IMAGES = [
                tk.PhotoImage(file=img_open),
                tk.PhotoImage(file=img_close),]
        else:
            cls.IMAGES[0].configure(file=img_open)
            cls.IMAGES[1].configure(file=img_close)


if __name__ == '__main__':
    root = tk.Tk()

    app = AccordionFrame(root)
    app.grid(sticky=tk.NSEW)

    top = app.winfo_toplevel()
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)

    g = app.add_group('g1', 'Tk widgets')
    l = tk.Label(g, text="Label1")
    l.grid()
    l = tk.Label(g, text="Label2")
    l.grid()
    g = app.add_group('g2', 'Ttk widgets')
    ##
    app = AccordionFrame(g)
    app.grid(sticky='nsew', padx="5 0")
    g = app.add_group('g1', 'Containers')
    l = tk.Label(g, text="Label1")
    l.grid()
    l = tk.Label(g, text="Label2")
    l.grid()
    g = app.add_group('g2', 'Control')
    l = tk.Label(g, text="Label3")
    l.grid()
    l = tk.Label(g, text="Label4")
    l.grid()

    tk.mainloop()
