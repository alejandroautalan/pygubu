import tkinter as tk
from pygubu.i18n import _
from pygubu.api.v1 import register_custom_property
from pygubu.widgets.pathchooserinput import PathChooserInput
from pygubu.plugins.pygubu._config import namespace, nspygubu

_builder_all = f"{namespace}.*"

_forms_all = f"{nspygubu.forms}.*"
_pathchoser_all = f"{nspygubu.widgets}.PathChooser.*"
_pathchoser_all_old = f"{nspygubu.builder_old}.pathchooser.*"

plugin_properties = dict(
    calendarfg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    calendarbg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    compound=[
        dict(
            buid=nspygubu.widgets.AccordionFrameGroup,
            editor="choice",
            values=(
                "",
                tk.LEFT,
                tk.RIGHT,
                tk.NONE,
            ),
            state="readonly",
        ),
        dict(
            buid=nspygubu.widgets.dockwidget,
            help=_(
                "Specifies how to display the image relative to the text, in the case both text and image are present."
            ),
        ),
    ],
    defaultextension=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        help=_("Dialog option. Sets default file extension."),
    ),
    expanded=dict(
        buid=nspygubu.widgets.AccordionFrameGroup,
        editor="choice",
        values=("", "false", "true"),
        state="readonly",
    ),
    field_name=[
        dict(buid=_forms_all, editor="fieldname_entry"),
        dict(
            buid=nspygubu.forms.ttkwidget.LabelWidgetInfo,
            editor="fieldname_selector",
        ),
    ],
    firstweekday=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="choice",
        values=("0", "6"),
        state="readonly",
        default_value="6",
    ),
    grouped=dict(
        buid=nspygubu.widgets.dockwidget,
        editor="choice",
        values=("", "true", "false"),
        state="readonly",
        help=_("When True, the widget is grouped within the container panel."),
    ),
    headerbg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    headerfg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    height=[
        dict(
            buid=nspygubu.widgets.AccordionFrame,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=nspygubu.widgets.hideableframe,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=nspygubu.forms.ttkwidget.FrameFormBuilder,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=[nspygubu.widgets.Dialog, nspygubu.builder_old.dialog],
            editor="dimensionentry",
            default_value=200,
        ),
    ],
    image=[
        dict(
            buid=[_pathchoser_all, _pathchoser_all_old],
            editor="imageentry",
            help=_("Image for the button."),
        ),
        dict(
            buid=nspygubu.widgets.dockwidget,
            editor="imageentry",
            help=_("Image to use as icon."),
        ),
    ],
    img_expand=dict(editor="imageentry"),
    img_collapse=dict(editor="imageentry"),
    initialdir=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        help=_("Dialog option. Sets initial directory."),
    ),
    keyvariable=dict(
        buid=[
            nspygubu.widgets.Combobox,
            nspygubu.builder_old.combobox,
            nspygubu.forms.pygubuwidget.PygubuCombobox,
        ],
        editor="tkvarentry",
        help=_("Tk variable associated to the key value."),
    ),
    label=dict(buid=nspygubu.widgets.AccordionFrameGroup),
    linewidth=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="choice",
        values=("1", "2", "3", "4"),
        state="readonly",
        default_value="1",
    ),
    mask=dict(buid=nspygubu.widgets.Floodgauge),
    markbg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    markfg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    maxsize=[
        dict(
            buid=[nspygubu.widgets.Dialog, nspygubu.builder_old.dialog],
            editor="whentry",
        ),
    ],
    minsize=[
        dict(
            buid=[nspygubu.widgets.Dialog, nspygubu.builder_old.dialog],
            editor="whentry",
        ),
    ],
    modal=[
        dict(
            buid=[nspygubu.widgets.Dialog, nspygubu.builder_old.dialog],
            editor="choice",
            values=("true", "false"),
            state="readonly",
            help=_("Determines if dialog is run in normal or modal mode."),
        ),
    ],
    month=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
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
    mustexist=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        editor="choice",
        values=("", "true", "false"),
        state="readonly",
        default_value="true",
        help=_(
            "Dialog option. Determines if path must exist for directory and file dialogs."
            + " The default value is True."
        ),
    ),
    path=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        help=_("Initial path value."),
    ),
    selectbg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    selectfg=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    show=dict(
        buid=[
            nspygubu.widgets.FilterableTreeview,
            nspygubu.widgets.EditableTreeview,
            nspygubu.builder_old.editabletreeview,
        ],
        editor="choice",
        values=("", "tree", "headings"),
        state="readonly",
    ),
    state=[
        dict(
            buid=[
                nspygubu.widgets.CalendarFrame,
                nspygubu.builder_old.calendarframe,
            ],
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
        ),
        dict(
            buid=[nspygubu.widgets.Combobox, nspygubu.builder_old.combobox],
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
            help=_("Combobox state."),
        ),
        dict(
            buid=nspygubu.forms.pygubuwidget.PygubuCombobox,
            editor="choice",
            values=("", "normal", "disabled"),
            state="readonly",
            help=_("Combobox state."),
        ),
        dict(
            buid=[_pathchoser_all, _pathchoser_all_old],
            editor="choice",
            values=("", "normal", "disabled", "readonly"),
            state="readonly",
            help=_("Path entry state."),
        ),
        dict(
            buid=[
                nspygubu.forms.ttkwidget.Entry,
                nspygubu.forms.ttkwidget.Combobox,
            ],
            editor="choice",
            values=("", "normal", "disabled", "readonly"),
            state="readonly",
        ),
    ],
    style=dict(
        buid=nspygubu.widgets.AccordionFrameGroup,
        editor="ttkstylechoice",
        default_value="Toolbutton",
    ),
    text=dict(
        buid=[nspygubu.widgets.Tooltip, nspygubu.widgets.Tooltipttk],
        editor="text",
        help=_("Text to display in tooltip."),
    ),
    textvariable=[
        dict(
            buid=[nspygubu.widgets.PathChooserButton],
            editor="tkvarentry",
            help=_(
                "Tk variable whose value will be used in place of the text resource."
            ),
        ),
        dict(
            buid=[_pathchoser_all, _pathchoser_all_old],
            editor="tkvarentry",
            help=_("Tk variable associated to the path property."),
        ),
    ],
    title=[
        dict(
            buid=[_pathchoser_all, _pathchoser_all_old],
            help=_("Dialog option. Sets dialog title."),
        ),
        dict(
            buid=nspygubu.widgets.dockwidget,
            help=_("Sets the widget title."),
        ),
    ],
    type=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        editor="choice",
        values=(PathChooserInput.FILE, PathChooserInput.DIR),
        state="readonly",
        default_value=PathChooserInput.FILE,
        help=_("Dialog type"),  # PathChooserInput
    ),
    value=dict(buid=nspygubu.widgets.ColorInput, editor="colorentry"),
    values=[
        dict(
            buid=[
                nspygubu.widgets.Combobox,
                nspygubu.builder_old.combobox,
                nspygubu.forms.pygubuwidget.PygubuCombobox,
            ],
            help=_(
                "In designer: json list of key, value pairs\n"
                '    Example: [["A", "Option 1 Label"], ["B", "Option 2 Label"]]\n'
                "In code: an iterable of key, value pairs"
            ),
        ),
    ],
    weight=[
        dict(
            buid=nspygubu.widgets.dockpane,
            editor="integernumber",
            help=_("The weight value for the pane."),
        ),
        dict(
            buid=nspygubu.widgets.dockwidget,
            editor="integernumber",
            help=_("The weight value of the widget in the pane"),
        ),
    ],
    width=[
        dict(
            buid=nspygubu.widgets.AccordionFrame,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=nspygubu.widgets.hideableframe,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(
            buid=nspygubu.forms.ttkwidget.FrameFormBuilder,
            editor="dimensionentry",
            default_value=200,
        ),
        dict(buid=nspygubu.widgets.PathChooserButton, editor="integernumber"),
        dict(
            buid=[nspygubu.widgets.Dialog, nspygubu.builder_old.dialog],
            editor="dimensionentry",
            default_value=200,
        ),
    ],
    xscrollcommand=dict(
        buid=[
            nspygubu.widgets.FilterableTreeview,
            nspygubu.widgets.EditableTreeview,
            nspygubu.builder_old.editabletreeview,
        ],
        editor="scrollsetcommandentry",
    ),
    year=dict(
        buid=[
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="naturalnumber",
    ),
    yscrollcommand=dict(
        buid=[
            nspygubu.widgets.FilterableTreeview,
            nspygubu.widgets.EditableTreeview,
            nspygubu.builder_old.editabletreeview,
        ],
        editor="scrollsetcommandentry",
    ),
)

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
