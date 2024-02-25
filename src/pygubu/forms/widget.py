class FieldWidget:
    def __init__(self, *args, field_name: str, **kw):
        super().__init__(*args, **kw)
        self.field_name = field_name

    def wset_value(self, value):
        # will set the value in the widget format
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wget_value(self):
        # Get value in the widget
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wmark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )

    def wis_disabled(self) -> bool:
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self.__class__}"
        )


class WidgetInfoBase:
    def __init__(self, *args, field_name: str, **kw):
        self.field_name = field_name
        super().__init__(*args, **kw)

    def show_error(self, error):
        raise NotImplementedError

    def show_help(self, message):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class WidgetInfo(WidgetInfoBase):
    pass


class FormInfo(WidgetInfoBase):
    pass
