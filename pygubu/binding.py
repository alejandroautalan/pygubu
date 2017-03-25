from __future__ import unicode_literals

__all__ = ['remove_binding', 'ApplicationLevelBindManager']

import platform
import logging


logger = logging.getLogger(__name__)

def bindings(widget, seq):
    return [x for x in widget.bind(seq).splitlines() if x.strip()]

def _funcid(binding):
    return binding.split()[1][3:]

def remove_binding(widget, seq, index=None, funcid=None):
    b = bindings(widget, seq)

    if not index is None:
        try:
            binding = b[index]
            widget.unbind(seq, _funcid(binding))
            b.remove(binding)
        except IndexError:
            logger.info('Binding #%d not defined.' % index)
            return

    elif funcid:
        binding = None
        for x in b:
            if _funcid(x) == funcid:
                binding = x
                b.remove(binding)
                widget.unbind(seq, funcid)
                break
        if not binding:
            logger.info( 'Binding "%s" not defined.' % funcid)
            return
    else:
        raise ValueError('No index or function id defined.')

    for x in b:
        widget.bind(seq, '+'+x, 1)


class ApplicationLevelBindManager(object):
    # Mouse wheel support
    mw_active_area = None
    mw_initialized = False

    @staticmethod
    def on_mousewheel(event):
        if ApplicationLevelBindManager.mw_active_area:
            ApplicationLevelBindManager.mw_active_area.on_mousewheel(event)
    
    @staticmethod
    def mousewheel_bind(widget):
        ApplicationLevelBindManager.mw_active_area = widget
    
    @staticmethod
    def mousewheel_unbind():
        ApplicationLevelBindManager.mw_active_area = None

    @staticmethod
    def init_mousewheel_binding(master):
        if ApplicationLevelBindManager.mw_initialized == False:
            _os = platform.system()
            if _os == "Linux" :
                master.bind_all('<4>', ApplicationLevelBindManager.on_mousewheel,  add='+')
                master.bind_all('<5>', ApplicationLevelBindManager.on_mousewheel,  add='+')
            else:
                # Windows and MacOS
                master.bind_all("<MouseWheel>", ApplicationLevelBindManager.on_mousewheel,  add='+')
            ApplicationLevelBindManager.mw_initialized = True

    @staticmethod
    def make_onmousewheel_cb(widget, orient, factor = 1):
        """Create a callback to manage mousewheel events
        
        orient: string (posible values: ('x', 'y'))
        widget: widget that implement tk xview and yview methods
        """
        _os = platform.system()
        view_command = getattr(widget, orient+'view')
        if _os == 'Linux':
            def on_mousewheel(event):
                if event.num == 4:
                    view_command("scroll",(-1)*factor,"units")
                elif event.num == 5:
                    view_command("scroll",factor,"units") 
        
        elif _os == 'Windows':
            def on_mousewheel(event):        
                view_command("scroll",(-1)*int((event.delta/120)*factor),"units") 
        
        elif _os == 'Darwin':
            def on_mousewheel(event):        
                view_command("scroll",event.delta,"units")             
        
        return on_mousewheel
