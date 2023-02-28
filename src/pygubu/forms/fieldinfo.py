class InfoDisplay:
    def __init__(self, *args, fname: str, **kw):
        self.fname = fname
        super().__init__(*args, **kw)

    def show_error(self, error):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class FieldInfoDisplay(InfoDisplay):
    ...


class FormInfoDisplay(InfoDisplay):
    ...
