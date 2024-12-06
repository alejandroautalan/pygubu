from tkcalendar import Calendar, DateEntry
from pygubu.plugins.tkcalendar.calendar import CalendarBO
from pygubu.plugins.tkcalendar.dateentry import DateEntryBO


class CalendarPreview(Calendar):
    """
    Temporary fix for recreating theme on every <<ThemeChanged>> event.
    """

    ...

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        self.theme_change_cbid = None
        self._theme_name = None
        self._setup_style_fixed()

        self.bind("<<ThemeChanged>>", self.schedule_style_update)

    def _setup_style(self, event=None):
        # Setup is ignored here on purpose.
        return None

    def _setup_style_fixed(self, event=None):
        super()._setup_style(event)
        self._theme_name = self.style.theme_use()

    def schedule_style_update(self, event=None):
        if self.theme_change_cbid is None:
            self.theme_change_cbid = self.after(10, self._on_theme_change)

    def _on_theme_change(self):
        theme = self.style.theme_use()
        if self._theme_name != theme:
            # the theme has changed, update the DateEntry style to look like a combobox
            self._theme_name = theme
            self._setup_style_fixed()
        self.theme_change_cbid = None


class DateEntryPreview(DateEntry):
    """
    Temporary fix for recreating theme on every <<ThemeChanged>> event.
    """

    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.theme_change_cbid = None
        self.bind("<<ThemeChanged>>", self.schedule_style_update)

    def _setup_style(self, event=None):
        super()._setup_style(event)
        self._theme_name = self.style.theme_use()

    def schedule_style_update(self, event=None):
        if self.theme_change_cbid is None:
            self.theme_change_cbid = self.after(10, self._on_theme_change)

    def _on_theme_change(self):
        theme = self.style.theme_use()
        if self._theme_name != theme:
            # the theme has changed, update the DateEntry style to look like a combobox
            self._theme_name = theme
            self._setup_style()
        self.theme_change_cbid = None


class CalendarPreviewBO(CalendarBO):
    class_ = CalendarPreview


class DateEntryPreviewBO(DateEntryBO):
    class_ = DateEntryPreview
