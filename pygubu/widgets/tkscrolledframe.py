# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
except:
    import Tkinter as tk

from pygubu import ApplicationLevelBindManager as BindManager
from pygubu.binding import remove_binding


class TkScrolledFrame(tk.Frame):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    BOTH = 'both'
    _framecls = tk.Frame
    _sbarcls = tk.Scrollbar

    def __init__(self, master=None, **kw):
        self.scrolltype = kw.pop('scrolltype', self.VERTICAL)
        self.usemousewheel = tk.getboolean(kw.pop('usemousewheel', False))
        self._bindingids = []

        #super(ScrolledFrameBase, self).__init__(master, **kw)
        self._framecls.__init__(self, master, **kw)

        self._container = self._framecls(self, width=200, height=200)
        self._clipper = self._framecls(self._container, width=200, height=200)
        self.innerframe = innerframe = self._framecls(self._clipper)
        self.vsb = vsb = self._sbarcls(self._container)
        self.hsb = hsb = self._sbarcls(self._container, orient="horizontal")

        # variables
        self.hsbOn = 0
        self.vsbOn = 0
        self.hsbNeeded = 0
        self.vsbNeeded = 0
        self._jfraction=0.05
        self._scrollTimer = None
        self._scrollRecurse = 0
        self._startX = 0
        self._startY = 0

        #configure scroll
        self.hsb.set(0.0, 1.0)
        self.vsb.set(0.0, 1.0)
        self.vsb.config(command=self.yview)
        self.hsb.config(command=self.xview)

        #grid
        self._container.pack(expand=True, fill='both')
        self._clipper.grid(row=0, column=0, sticky=tk.NSEW)
        #self.vsb.grid(row=0, column=1, sticky=tk.NS)
        #self.hsb.grid(row=1, column=0, sticky=tk.EW)
        
        self._container.rowconfigure(0, weight=1)
        self._container.columnconfigure(0, weight=1)

        # Whenever the clipping window or scrolled frame change size,
        # update the scrollbars.
        self.innerframe.bind('<Configure>', self._reposition)
        self._clipper.bind('<Configure>', self._reposition)
        self.bind('<Configure>', self._reposition)
        self._configure_mousewheel()

    # Set timer to call real reposition method, so that it is not
    # called multiple times when many things are reconfigured at the
    # same time.
    def reposition(self):
        if self._scrollTimer is None:
            self._scrollTimer = self.after_idle(self._scrollBothNow)

    # Called when the user clicks in the horizontal scrollbar.
    # Calculates new position of frame then calls reposition() to
    # update the frame and the scrollbar.
    def xview(self, mode = None, value = None, units = None):
        if type(value) == str:
            value = float(value)
        if mode is None:
            return self.hsb.get()
        elif mode == 'moveto':
            frameWidth = self.innerframe.winfo_reqwidth()
            self._startX = value * float(frameWidth)
        else: # mode == 'scroll'
            clipperWidth = self._clipper.winfo_width()
            if units == 'units':
                jump = int(clipperWidth * self._jfraction)
            else:
                jump = clipperWidth
            self._startX = self._startX + value * jump

        self.reposition()

    # Called when the user clicks in the vertical scrollbar.
    # Calculates new position of frame then calls reposition() to
    # update the frame and the scrollbar.
    def yview(self, mode = None, value = None, units = None):

        if type(value) == str:
            value = float(value)
        if mode is None:
            return self.vsb.get()
        elif mode == 'moveto':
            frameHeight = self.innerframe.winfo_reqheight()
            self._startY = value * float(frameHeight)
        else: # mode == 'scroll'
            clipperHeight = self._clipper.winfo_height()
            if units == 'units':
                jump = int(clipperHeight * self._jfraction)
            else:
                jump = clipperHeight
            self._startY = self._startY + value * jump

        self.reposition()

    def _reposition(self, event):
        self.reposition()

    def _getxview(self):

        # Horizontal dimension.
        clipperWidth = self._clipper.winfo_width()
        frameWidth = self.innerframe.winfo_reqwidth()
        if frameWidth <= clipperWidth:
            # The scrolled frame is smaller than the clipping window.

            self._startX = 0
            endScrollX = 1.0
            #use expand by default
            relwidth = 1
        else:
            # The scrolled frame is larger than the clipping window.
            #use expand by default
            if self._startX + clipperWidth > frameWidth:
                self._startX = frameWidth - clipperWidth
                endScrollX = 1.0
            else:
                if self._startX < 0:
                    self._startX = 0
                endScrollX = (self._startX + clipperWidth) / float(frameWidth)
            relwidth = ''

        # Position frame relative to clipper.
        self.innerframe.place(x = -self._startX, relwidth = relwidth)
        return (self._startX / float(frameWidth), endScrollX)

    def _getyview(self):

        # Vertical dimension.
        clipperHeight = self._clipper.winfo_height()
        frameHeight = self.innerframe.winfo_reqheight()
        if frameHeight <= clipperHeight:
            # The scrolled frame is smaller than the clipping window.

            self._startY = 0
            endScrollY = 1.0
            # use expand by default
            relheight = 1
        else:
            # The scrolled frame is larger than the clipping window.
            # use expand by default
            if self._startY + clipperHeight > frameHeight:
                self._startY = frameHeight - clipperHeight
                endScrollY = 1.0
            else:
                if self._startY < 0:
                    self._startY = 0
                endScrollY = (self._startY + clipperHeight) / float(frameHeight)
            relheight = ''

        # Position frame relative to clipper.
        self.innerframe.place(y = -self._startY, relheight = relheight)
        return (self._startY / float(frameHeight), endScrollY)

    # According to the relative geometries of the frame and the
    # clipper, reposition the frame within the clipper and reset the
    # scrollbars.
    def _scrollBothNow(self):
        self._scrollTimer = None

        # Call update_idletasks to make sure that the containing frame
        # has been resized before we attempt to set the scrollbars.
        # Otherwise the scrollbars may be mapped/unmapped continuously.
        self._scrollRecurse = self._scrollRecurse + 1
        self.update_idletasks()
        self._scrollRecurse = self._scrollRecurse - 1
        if self._scrollRecurse != 0:
            return

        xview = self._getxview()
        yview = self._getyview()
        self.hsb.set(xview[0], xview[1])
        self.vsb.set(yview[0], yview[1])

        require_hsb = self.scrolltype in (self.BOTH, self.HORIZONTAL)
        self.hsbNeeded = (xview != (0.0, 1.0)) and require_hsb
        require_vsb = self.scrolltype in (self.BOTH, self.VERTICAL)
        self.vsbNeeded = (yview != (0.0, 1.0)) and require_vsb

        # If both horizontal and vertical scrollmodes are dynamic and
        # currently only one scrollbar is mapped and both should be
        # toggled, then unmap the mapped scrollbar.  This prevents a
        # continuous mapping and unmapping of the scrollbars.
        if (self.hsbNeeded != self.hsbOn and
            self.vsbNeeded != self.vsbOn and
            self.vsbOn != self.hsbOn):
            if self.hsbOn:
                self._toggleHorizScrollbar()
            else:
                self._toggleVertScrollbar()
            return

        if self.hsbNeeded != self.hsbOn:
            self._toggleHorizScrollbar()

        if self.vsbNeeded != self.vsbOn:
            self._toggleVertScrollbar()

    def _toggleHorizScrollbar(self):

        self.hsbOn = not self.hsbOn

        #interior = self #.origInterior
        if self.hsbOn:
            self.hsb.grid(row=1, column=0, sticky=tk.EW)
            #interior.grid_rowconfigure(3, minsize = self['scrollmargin'])
        else:
            self.hsb.grid_forget()
            #interior.grid_rowconfigure(3, minsize = 0)

    def _toggleVertScrollbar(self):

        self.vsbOn = not self.vsbOn

        #interior = self#.origInterior
        if self.vsbOn:
            self.vsb.grid(row=0, column=1, sticky=tk.NS)
            #interior.grid_columnconfigure(3, minsize = self['scrollmargin'])
        else:
            self.vsb.grid_forget()
            #interior.grid_columnconfigure(3, minsize = 0)

    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'usemousewheel'
        if key in args:
            self.usemousewheel = tk.getboolean(args[key])
            del args[key]
            self._configure_mousewheel()
        #super(ScrolledFrameBase, self).configure(args)
        self._framecls.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'usemousewheel'
        if key == option:
            return self.usemousewheel
        #return super(ScrolledFrameBase, self).cget(key)
        return self._framecls.cget(self, key)

    __getitem__ = cget

    def _configure_mousewheel(self):
        if self.usemousewheel:
            BindManager.init_mousewheel_binding(self)

            if self.hsb and not hasattr(self.hsb, 'on_mousewheel'):
                self.hsb.on_mousewheel = BindManager.make_onmousewheel_cb(self, 'x', 2)
            if self.vsb and not hasattr(self.vsb, 'on_mousewheel'):
                self.vsb.on_mousewheel = BindManager.make_onmousewheel_cb(self, 'y', 2)

            main_sb = self.vsb or self.hsb
            if main_sb:
                self.on_mousewheel = main_sb.on_mousewheel
                bid = self.bind('<Enter>',
                                lambda event: BindManager.mousewheel_bind(self),
                                add='+')
                self._bindingids.append((self, bid))
                bid = self.bind('<Leave>',
                                lambda event: BindManager.mousewheel_unbind(),
                                add='+')
                self._bindingids.append((self, bid))
            for s in (self.vsb, self.hsb):
                if s:
                    bid = s.bind('<Enter>',
                                 lambda event, scrollbar=s: BindManager.mousewheel_bind(scrollbar),
                                 add='+')
                    self._bindingids.append((s, bid))
                    if s != main_sb:
                        bid = s.bind('<Leave>',
                                     lambda event: BindManager.mousewheel_unbind(),
                                     add='+')
                        self._bindingids.append((s, bid))
        else:
            for widget, bid in self._bindingids:
                remove_binding(widget, bid)


#class TkScrolledFrameFactory(type):
#    def __new__(cls, clsname, superclasses, attrs):
#        return type.__new__(cls, str(clsname), superclasses, attrs)


#TkScrolledFrame = TkScrolledFrameFactory('TkScrolledFrame',
#                                       (ScrolledFrameBase, tk.Frame, object),
#                                       {'_framecls':tk.Frame,
#                                        '_sbarcls': tk.Scrollbar})
