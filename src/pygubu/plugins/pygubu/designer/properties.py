import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.plugins.pygubu import _plugin_uid
from pygubu.plugins.pygubu.forms.base import _plugin_forms_uid as forms_uid
from pygubu.widgets.pathchooserinput import PathChooserInput


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
_forms_all = f"{forms_uid}.*"
_forms_PygubuCombobox = f"{forms_uid}.pygubuwidget.PygubuCombobox"
_forms_FrameFormBuilder = f"{forms_uid}.ttkwidget.FrameFormBuilder"
_forms_LabelWidgetInfo = f"{forms_uid}.ttkwidget.LabelWidgetInfo"
_forms_Combobox = f"{forms_uid}.ttkwidget.Combobox"
_HideableFrame = f"{_plugin_uid}.hideableframe"
_PathChoser_all = f"{_plugin_uid}.PathChooser.*"
_PathChoser_old = "pygubu.builder.widgets.pathchooser.*"
_PathChoserButton = f"{_plugin_uid}.PathChooserButton"

h_values = _(
    "In designer: json list of key, value pairs\n"
    '    Example: [["A", "Option 1 Label"], ["B", "Option 2 Label"]]\n'
    "In code: an iterable of key, value pairs"
)  # combobox
h_keyvariable = _("Tk variable associated to the key value.")  # combobox
h_state = _("Combobox state.")  # combobox
h_modal = _("Determines if dialog is run in normal or modal mode.")  # Dialog
h_weight = _("The weight value for the pane.")  # DockPane
h_mustexist = _(
    "Dialog option. Determines if path must exist for directory and file dialogs."
    + " The default value is True."
)  # PathChooserInput
h_initialdir = _("Dialog option. Sets initial directory.")  # PathChooserInput
h_title = _("Dialog option. Sets dialog title.")  # PathChooserInput
h_defaultextension = _help = _("Dialog option. Sets default file extension.")

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
    "defaultextension": dict(
        buid=[_PathChoser_all, _PathChoser_old], help=h_defaultextension
    ),
    "expanded": dict(
        buid=_AccordionFrameGroup,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
    ),
    "field_name": [
        dict(buid=_forms_all, editor="fieldname_entry"),
        dict(buid=_forms_LabelWidgetInfo, editor="fieldname_selector"),
    ],
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
        dict(buid=_AccordionFrame, editor="dimensionentry", default_value=200),
        dict(buid=_HideableFrame, editor="dimensionentry", default_value=200),
        dict(
            buid=_forms_FrameFormBuilder,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=[_Dialog, _Dialog_old],
            editor="dimensionentry",
            default_value=200,
        ),
    ],
    "image": dict(
        buid=[_PathChoser_all, _PathChoser_old],
        editor="imageentry",
        help=_("Image for the button."),
    ),
    "img_expand": dict(editor="imageentry"),
    "img_collapse": dict(editor="imageentry"),
    "initialdir": dict(
        buid=[_PathChoser_all, _PathChoser_old], help=h_initialdir
    ),
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
    "mustexist": dict(
        buid=[_PathChoser_all, _PathChoser_old],
        editor="choice",
        values=("", "true", "false"),
        state="readonly",
        default_value="true",
        help=h_mustexist,
    ),
    "path": dict(
        buid=[_PathChoser_all, _PathChoser_old],
        help=_("Initial path value."),
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
        dict(
            buid=[_PathChoser_all, _PathChoser_old],
            editor="choice",
            values=("", "normal", "disabled", "readonly"),
            state="readonly",
            help=_("Path entry state."),
        ),
        dict(
            buid=_forms_Combobox,
            editor="choice",
            values=("", "normal", "disabled", "readonly"),
            state="readonly",
        ),
    ],
    "style": dict(
        buid=_AccordionFrameGroup,
        editor="ttkstylechoice",
        default_value="Toolbutton",
    ),
    "textvariable": [
        dict(
            buid=[_PathChoserButton],
            editor="tkvarentry",
            help=_(
                "Tk variable whose value will be used in place of the text resource."
            ),
        ),
        dict(
            buid=[_PathChoser_all, _PathChoser_old],
            editor="tkvarentry",
            help=_("Tk variable associated to the path property."),
        ),
    ],
    "title": dict(buid=[_PathChoser_all, _PathChoser_old], help=h_title),
    "type": dict(
        buid=[_PathChoser_all, _PathChoser_old],
        editor="choice",
        values=(PathChooserInput.FILE, PathChooserInput.DIR),
        state="readonly",
        default_value=PathChooserInput.FILE,
        help=_("Dialog type"),  # PathChooserInput
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
        dict(
            buid=_forms_FrameFormBuilder,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(buid=_PathChoserButton, editor="integernumber"),
        dict(
            buid=[_Dialog, _Dialog_old],
            editor="dimensionentry",
            default_value=200,
        ),
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
