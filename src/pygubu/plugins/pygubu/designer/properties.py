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
            nspygubu.widgets.CalendarView,
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    calendarbg=dict(
        buid=[
            nspygubu.widgets.CalendarView,
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
            help=_("Icon position in the header."),
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
        help=_("Determine if group is shown expanded or collapsed."),
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
            nspygubu.widgets.CalendarView,
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="choice",
        values=("0", "6"),
        state="readonly",
        default_value="6",
    ),
    grid_anchor=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice",
        values=(
            "nw",
            "n",
            "ne",
            "w",
            "center",
            "e",
            "sw",
            "s",
            "se",
        ),
        state="readonly",
        default_value="center",
        help=_(
            "The anchor value controls how to place the grid within the container window when no row/column has any weight."
        ),
    ),
    grid_dim_rows=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice",
        values=["auto", "1", "2", "3", "4", "5", "0, 1, 0"],
        default_value="auto",
        help=_(
            """Rows dimension specfication
Allowed values:
  Literal string "auto": automatic rows
  Integer "x": Grid has x rows
  List of comma separated weights "0, 1, 0": Grid has len(weights) rows.
  """
        ),
    ),
    grid_dim_cols=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice",
        values=["auto", "1", "2", "0, 1, 0"],
        default_value="auto",
        help=_(
            """Columns dimension specfication
Allowed values:
  Literal string "auto": automatic columns
  Integer "y": Grid has y rows
  List of comma separated weights "0, 1, 0": Grid has len(weights) columns.
  """
        ),
    ),
    grid_flow=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice_key",
        values=[
            ("row", "Row"),
            ("column", "Column"),
        ],
        state="readonly",
        default_value="row",
        help=_(
            "Controls the direction children are placed when flowing across the grid.\nDefault is 'row' (left-to-right, then next row). Use 'column' to fill down first, then move to the next column."
        ),
    ),
    grid_expand=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice",
        values=("True", "False"),
        state="readonly",
        default_value="False",
        help=_("Take all available space in the frame cavity."),
    ),
    grid_propagate=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice",
        values=("True", "False"),
        state="readonly",
        default_value="True",
        help=_("Enable/Disable Geometry Propagation"),
    ),
    grid_chsizing=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice_key",
        values=[
            ("fill", "Fill"),
            ("shrink_begin", "Shrink Begin"),
            ("shrink_center", "Shrink Center"),
            ("shrink_end", "Shrink End"),
        ],
        state="readonly",
        default_value="shrink_center",
        help=_("Horizontal sizing for each grid cell."),
    ),
    grid_cvsizing=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="choice_key",
        values=[
            ("fill", "Fill"),
            ("shrink_begin", "Shrink Begin"),
            ("shrink_center", "Shrink Center"),
            ("shrink_end", "Shrink End"),
        ],
        state="readonly",
        default_value="shrink_center",
        help=_("Vertical sizing for each grid cell."),
    ),
    grid_gap=dict(
        buid=[nspygubu.widgets.GridFrame],
        editor="twodimensionentry",
        default_value="0",
        help=_(
            "Gap between rows and columns.\nAccepts two dimensions values, one for rows and one for columns. If one dimension is supplied, it applies to both.\n"
        ),
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
            nspygubu.widgets.CalendarView,
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    headerfg=dict(
        buid=[
            nspygubu.widgets.CalendarView,
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
            nspygubu.widgets.CalendarView,
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
            nspygubu.widgets.CalendarView,
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    markfg=dict(
        buid=[
            nspygubu.widgets.CalendarView,
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
            nspygubu.widgets.CalendarView,
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
    pack_alignment=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice_key",
        values=[
            ("begin", "Begin"),
            ("center", "Center"),
            ("end", "End"),
        ],
        state="readonly",
        default_value="begin",
        help=_("Positioning of the pack when not expanded."),
    ),
    pack_direction=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice_key",
        values=[
            ("row", "Horizontal"),
            ("column", "Vertical"),
        ],
        state="readonly",
        default_value="row",
        help=_("Box direction or flow."),
    ),
    pack_expand=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice",
        values=("True", "False"),
        state="readonly",
        default_value="False",
        help=_("Take all available space in the frame cavity."),
    ),
    pack_chsizing=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice_key",
        values=[
            ("fill", "Fill"),
            ("shrink_begin", "Shrink Begin"),
            ("shrink_center", "Shrink Center"),
            ("shrink_end", "Shrink End"),
        ],
        state="readonly",
        default_value="shrink_center",
        help=_("Horizontal sizing for each pack cell."),
    ),
    pack_cvsizing=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice_key",
        values=[
            ("fill", "Fill"),
            ("shrink_begin", "Shrink Begin"),
            ("shrink_center", "Shrink Center"),
            ("shrink_end", "Shrink End"),
        ],
        state="readonly",
        default_value="shrink_center",
        help=_("Vertical sizing for each pack cell."),
    ),
    pack_gap=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="dimensionentry",
        default_value="0",
        help=_("Gap applied between each pack cell."),
    ),
    pack_propagate=dict(
        buid=[nspygubu.widgets.PackFrame],
        editor="choice",
        values=("True", "False"),
        state="readonly",
        default_value="True",
        help=_("Enable/Disable Geometry Propagation"),
    ),
    path=dict(
        buid=[_pathchoser_all, _pathchoser_all_old],
        help=_("Initial path value."),
    ),
    selectbg=dict(
        buid=[
            nspygubu.widgets.CalendarView,
            nspygubu.widgets.CalendarFrame,
            nspygubu.builder_old.calendarframe,
        ],
        editor="colorentry",
    ),
    selectfg=dict(
        buid=[
            nspygubu.widgets.CalendarView,
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
                nspygubu.widgets.CalendarView,
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
            nspygubu.widgets.CalendarView,
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
