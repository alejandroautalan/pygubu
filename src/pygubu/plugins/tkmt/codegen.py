class TkmtWidgetCodeMixin:
    def code_configure(self, targetid=None):
        return []

    def code_connect_commands(self):
        return []

    def _code_process_pos_kw_properties(self, code_identifier):
        """Creates dict with properties values for code"""
        defaults = self._get_property_defaults()
        args = {}
        for rop in self.properties:
            value_is_set = False
            pvalue = None
            if rop in self.wmeta.properties:
                pvalue = self.wmeta.properties[rop]
                value_is_set = True
            elif rop in defaults:
                pvalue = defaults[rop]
                value_is_set = True
            if value_is_set:
                pvalue = self._code_process_property_value(
                    code_identifier, rop, pvalue
                )
                args[rop] = pvalue
        return args

    def code_realize(self, boparent, code_identifier=None):
        if code_identifier is not None:
            self._code_identifier = code_identifier
        lines = []
        master = boparent.code_child_master()

        pbag = self._code_process_pos_kw_properties(code_identifier)
        kargs = self._get_keyword_args(pbag)
        args = self._get_positional_args(pbag)

        pos_args = ""
        if args:
            pos_args = ",".join(args)

        bag = []
        for pname, value in kargs.items():
            bag.append(f"{pname}={value}")

        kwargs = ""
        if bag:
            if args:
                kwargs = f""", {", ".join(bag)}"""
            else:
                kwargs = ", ".join(bag)
        s = f"{self.code_identifier()} = {self._code_class_name()}({pos_args}{kwargs})"
        if hasattr(self, "master_add_method"):
            method = self.master_add_method
            s = f"{self.code_identifier()} = {master}.{method}({pos_args}{kwargs})"
        lines.append(s)
        return lines
