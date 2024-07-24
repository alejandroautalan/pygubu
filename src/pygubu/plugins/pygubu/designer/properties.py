import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.pygubu import _designer_tab_label, _plugin_uid
from pygubu.plugins.pygubu.forms.base import _plugin_uid as forms_uid


_builder_all = f"{_plugin_uid}.*"
_AccordionFrame = f"{_plugin_uid}.AccordionFrame"
_AccordionFrameGroup = f"{_plugin_uid}.AccordionFrameGroup"
_CalendarFrame = f"{_plugin_uid}.CalendarFrame"
_CalendarFrame_old = "pygubu.builder.widgets.calendarframe"
_ColorInput = f"{_plugin_uid}.ColorInput"
_Combobox = f"{_plugin_uid}.Combobox"
_Combobox_old = "pygubu.builder.widgets.combobox"
_Dialog = f"{_plugin_uid}.Dialog"
_Dialog_old = "pygubu.builder.widgets.dialog"
_DockFrame = f"{_plugin_uid}.docframe"
_DockPane = f"{_plugin_uid}.docpane"
_DockWidget = f"{_plugin_uid}.dockwidget"
_forms_PygubuCombobox = f"{forms_uid}.pygubuwidget.PygubuCombobox"
_HideableFrame = f"{_plugin_uid}.hideableframe"

h_values = _(
    "In designer: json list of key, value pairs\n"
    '    Example: [["A", "Option 1 Label"], ["B", "Option 2 Label"]]\n'
    "In code: an iterable of key, value pairs"
)  # combobox
h_keyvariable = _("Tk variable associated to the key value.")  # combobox
h_state = _("Combobox state.")  # combobox
h_modal = _("Determines if dialog is run in normal or modal mode.")  # Dialog
h_weight = _("The weight value for the pane.")  # DockPane

plugin_properties = {
    "calendarfg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "calendarbg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "compound": dict(
        buid=_AccordionFrameGroup,
        editor="choice",
        values=(
            "",
            tk.LEFT,
            tk.RIGHT,
            tk.NONE,
        ),
        state="readonly",
    ),
    "firstweekday": dict(
        buid=[_CalendarFrame, _CalendarFrame_old],
        editor="choice",
        values=("0", "6"),
        state="readonly",
        default_value="6",
    ),
    "grouped": dict(
        buid=_DockWidget,
        editor="choice",
        values=("", "true", "false"),
        state="readonly",
    ),
    "headerbg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "headerfg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "height": [
        dict(
            buid=_AccordionFrame, editor="dimensionentry", default_value="200"
        ),
        dict(buid=_HideableFrame, editor="dimensionentry", default_value=200),
    ],
    "img_expand": dict(editor="imageentry"),
    "img_collapse": dict(editor="imageentry"),
    "keyvariable": dict(
        buid=[_Combobox, _Combobox_old, _forms_PygubuCombobox],
        editor="tkvarentry",
        help=h_keyvariable,
    ),
    "label": dict(buid=_AccordionFrameGroup),
    "linewidth": dict(
        buid=[_CalendarFrame, _CalendarFrame_old],
        editor="choice",
        values=("1", "2", "3", "4"),
        state="readonly",
        default_value="1",
    ),
    "mask": dict(buid=f"{_plugin_uid}.Floodgauge"),
    "markbg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "markfg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "modal": [
        dict(
            buid=[_Dialog, _Dialog_old],
            editor="choice",
            values=("true", "false"),
            state="readonly",
            help=h_modal,
        ),
    ],
    "month": dict(
        buid=[_CalendarFrame, _CalendarFrame_old],
        editor="choice",
        values=(
            "",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ),
        state="readonly",
    ),
    "selectbg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "selectfg": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="colorentry"
    ),
    "state": [
        dict(
            buid=[_CalendarFrame, _CalendarFrame_old],
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
        ),
        dict(
            buid=[_Combobox, _Combobox_old],
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
            help=h_state,
        ),
        dict(
            buid=_forms_PygubuCombobox,
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
            help=h_state,
        ),
    ],
    "style": dict(
        buid=_AccordionFrameGroup,
        editor="ttkstylechoice",
        default_value="Toolbutton",
    ),
    "expanded": dict(
        buid=_AccordionFrameGroup,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
    ),
    "value": dict(buid=_ColorInput, editor="colorentry"),
    "values": [
        dict(
            buid=[_Combobox, _Combobox_old, _forms_PygubuCombobox],
            help=h_values,
        ),
    ],
    "weight": [
        dict(buid=_DockPane, editor="integernumber", help=h_weight),
        dict(
            buid=_DockWidget,
            editor="integernumber",
            help=_("The weight value of the widget in the pane"),
        ),
    ],
    "width": [
        dict(buid=_AccordionFrame, editor="dimensionentry", default_value=200),
        dict(buid=_HideableFrame, editor="dimensionentry", default_value=200),
    ],
    "year": dict(
        buid=[_CalendarFrame, _CalendarFrame_old], editor="naturalnumber"
    ),
}

for prop in plugin_properties:
    definitions = plugin_properties[prop]
    if isinstance(definitions, dict):
        definitions = [definitions]
    for definition in definitions:
        builders = definition.pop("buid", _builder_all)
        if isinstance(builders, str):
            builders = [builders]
        editor = definition.pop("editor", "entry")
        for builder_uid in builders:
            register_custom_property(builder_uid, prop, editor, **definition)
