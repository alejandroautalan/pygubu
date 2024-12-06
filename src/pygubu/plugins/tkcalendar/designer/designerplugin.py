from pygubu.api.v1 import IDesignerPlugin
from .properties import _calendar, _dateentry
from .previewhelper import CalendarPreviewBO, DateEntryPreviewBO


class TkcalendarPlugin(IDesignerPlugin):
    def get_preview_builder(self, builder_uid: str):
        if builder_uid == _calendar:
            return CalendarPreviewBO
        elif builder_uid == _dateentry:
            return DateEntryPreviewBO
        return None
