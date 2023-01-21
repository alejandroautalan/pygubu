from pygubu.api.v1 import BuilderObject


class AutocompleteBaseBO(BuilderObject):
    init_completevalues = True

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)
        if self.init_completevalues:
            prop = "completevalues"
            if prop not in self.wmeta.properties:
                args[prop] = ""
        return args

    def _process_property_value(self, pname, value):
        final_value = value
        if pname == "completevalues":
            final_value = value.split()
        else:
            final_value = super(
                AutocompleteBaseBO, self
            )._process_property_value(pname, value)
        return final_value

    def _code_process_property_value(self, targetid, pname, value):
        if pname == "completevalues":
            cvalues = None
            try:
                cvalues = f"{value.split()}"
            except Exception:
                pass
            return cvalues
        return super()._code_process_property_value(targetid, pname, value)


class CallbakInitArgMixin:
    """Some widgtes of the ttkwidget set, have a callback argument in the
    constructor and the widget does not allow to use configure method
    to modify it.
    So create a mixin class to configure the callback with a trick.
    """

    def _get_init_args(self, extra_init_args: dict = None):
        args = super()._get_init_args(extra_init_args)

        class CBProxy:
            def __init__(self):
                self.real_cb = None

            def __call__(self, family):
                if self.real_cb is not None:
                    self.real_cb(family)

        args["callback"] = cb = CBProxy()
        self._cb_proxy = cb
        return args

    def _connect_command(self, cmd_pname, callback):
        # continue the trick for setting the callback init argument
        if cmd_pname == "callback":
            self._cb_proxy.real_cb = callback
        else:
            super(CallbakInitArgMixin, self)._connect_command(
                cmd_pname, callback
            )

    def _code_get_init_args(self, code_identifier):
        args = super(CallbakInitArgMixin, self)._code_get_init_args(
            code_identifier
        )
        pname = "callback"
        if pname in self.wmeta.properties:
            pvalue = self.wmeta.properties[pname]
            args["callback"] = self._code_process_property_value(
                code_identifier, pname, pvalue
            )
        return args

    def _code_connect_command(self, cmd_pname, cmd, cbname):
        if cmd_pname == "callback":
            return []
        else:
            return super(CallbakInitArgMixin, self)._code_connect_command(
                cmd_pname, cmd, cbname
            )
