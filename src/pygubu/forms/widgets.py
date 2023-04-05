"""Widget related classes"""
import json


class WidgetManager:
    def __init__(self, field):
        self._field = field


class DataManager(WidgetManager):

    # Field Widget Data Manager
    # This class will help user to customize widget data management.

    def set_value(self, value):
        # will set the value in the widget format
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self._field.__class__}"
        )

    def get_value(self):
        # Get value in the widget
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self._field.__class__}"
        )

    def to_python(self, value):
        # will return a python object representation of value"
        # should raise ValidationError if value can't be converted.
        #
        # First field.to_python is called and the result is passed
        # to this method.
        return value

    def validate(self, value):
        # field specific validation.
        # should raise ValidationError if invalid
        pass

    @property
    def data(self):
        return self.get_value()

    @data.setter
    def data(self, value):
        self.set_value(value)


class ViewManager(WidgetManager):
    def mark_invalid(self, state: bool):
        # Visually mark the widget as invalid depending on state parameter.
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self._field.__class__}"
        )

    def is_disabled(self) -> bool:
        raise NotImplementedError(
            f"Subclasses must define this method. {self.__class__}"
            f" for field class {self._field.__class__}"
        )

    @property
    def disabled(self):
        return self.is_disabled()


class FieldWidget:
    class DataManager(DataManager):
        pass

    class ViewManager(ViewManager):
        pass

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        # Subclasess should set its own widget manager
        self.wdata: DataManager = self.DataManager(self)
        self.wview: ViewManager = self.ViewManager(self)

    def mark_invalid(self, state: bool):
        if self.wview is None:
            raise RuntimeError("View manager not set")
        self.wview.mark_invalid(state)

    @property
    def disabled(self):
        if self.wview is None:
            raise RuntimeError("View manager not set")
        return self.wview.disabled


class CallableChoiceIterator:
    def __init__(self, choices_func):
        self.choices_func = choices_func

    def __iter__(self):
        yield from self.choices_func()


class ChoiceWidget(FieldWidget):
    def __init__(self, *args, choices=None, **kw):
        super().__init__(*args, **kw)
        self.choices = () if choices is None else choices

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        # Setting choices also sets the choices on the widget.
        # choices can be any iterable, but we call list() on it because
        # it will be consumed more than once.
        if callable(value):
            value = CallableChoiceIterator(value)
        elif isinstance(value, str):
            value = self._strto_choices(value)
        else:
            value = list(value)

        self._choices = value

    @property
    def choices(self):
        return self._get_choices()

    @choices.setter
    def choices(self, value):
        self._set_choices(value)

    def valid_value(self, value):
        if value and (value in self._choices):
            return True
        return False

    def _strto_choices(self, value):
        try:
            choices = json.loads(value)
            if isinstance(choices, list):
                return choices
            else:
                raise ValueError("Json value must be a list")
        except json.JSONDecodeError:
            raise ValueError("Can't decode json value")
