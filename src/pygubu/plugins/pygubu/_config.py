from pygubu.utils.namespace import walkns, SN
from pygubu.i18n import _
from pygubu.plugins import (
    GROOT,
    GCONTAINER,
    GDISPLAY,
    GINPUT,
)

_section_label_containers = _("Pygubu Containers")
_section_label_widgets = _("Pygubu Control & Display")
_section_label_helpers = _("Pygubu Helpers")
_section_label_forms = _("Pygubu Forms")

_section_containers = ("ttk", _section_label_containers)
_section_containers_tk = ("tk", _section_label_containers)
_section_widgets = ("ttk", _section_label_widgets)
_section_widgets_tk = ("tt", _section_label_widgets)
_section_helpers_tk = ("tk", _section_label_helpers)
_section_helpers_ttk = ("ttk", _section_label_helpers)
_section_forms = ("ttk", _section_label_forms)

namespace = "pygubu"

ns_pygubu = SN(
    _name=namespace,
    widgets=SN(
        _name="widgets",
        AccordionFrame=1,
        AccordionFrameGroup=1,
        CalendarFrame=1,  # Deprecated
        CalendarView=1,
        ColorInput=1,
        Combobox=1,
        Dialog=1,
        EditableTreeview=1,
        FilterableTreeview=1,
        Floodgauge=1,
        FontInput=1,
        PathChooserInput=1,
        PathChooserButton=1,
        ScrollbarHelper=1,
        ScrolledFrame=1,
        Tooltip=1,
        Tooltipttk=1,
        TkScrollbarHelper=1,
        TkScrolledFrame=1,
        dockframe=1,
        dockpane=1,
        dockwidget=1,
        hideableframe=1,
        BoxFrame=1,
    ),
    forms=SN(
        _name="forms",
        tkwidget=SN(
            _name="tkwidget",
            Text=1,
        ),
        ttkwidget=SN(
            _name="ttkwidget",
            FrameFormBuilder=1,
            Label=1,
            Entry=1,
            LabelWidgetInfo=1,
            Combobox=1,
            Checkbutton=1,
        ),
        pygubuwidget=SN(
            _name="pygubuwidget",
            PygubuCombobox=1,
            FontInput=1,
            ColorInput=1,
        ),
    ),
    builder_old=SN(
        _name="builder.widgets",
        calendarframe=1,
        combobox=1,
        dialog=1,
        editabletreeview=1,
        pathchooserinput=1,
        scrollbarhelper=1,
        scrolledframe=1,
        tkscrollbarhelper=1,
        tkscrolledframe=1,
        tkinterscrolledtext=1,
        Labelwidget=1,
        toplevelmenu=1,
    ),
)

nspygubu = walkns(ns_pygubu)
