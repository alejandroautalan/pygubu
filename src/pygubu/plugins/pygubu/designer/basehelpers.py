from pygubu.api.v1 import BuilderObject
from pygubu.plugins.tk.tkstdwidgets import TKToplevel


class ToplevelPreviewFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, str(clsname), superclasses, attrs)


class ToplevelPreviewMixin(object):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.tl_attrs = {}
        self._w_set = False
        self._h_set = False

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        key = "width"
        if key in kw:
            value = int(kw[key])
            minsize = self.tl_attrs.get("minsize", None)
            maxsize = self.tl_attrs.get("maxsize", None)
            remove = False
            if minsize and value < minsize[0]:
                remove = True
            if maxsize and value > maxsize[0]:
                remove = True
            if self._w_set:
                resizable = self.tl_attrs.get("resizable", None)
                if resizable and not TKToplevel.RESIZABLE[resizable][0]:
                    remove = True
            if remove:
                kw.pop(key)
            else:
                self._w_set = True
        key = "height"
        if key in kw:
            value = int(kw[key])
            minsize = self.tl_attrs.get("minsize", None)
            maxsize = self.tl_attrs.get("maxsize", None)
            remove = False
            if minsize and value < minsize[1]:
                remove = True
            if maxsize and value > maxsize[1]:
                remove = True
            if self._h_set:
                resizable = self.tl_attrs.get("resizable", None)
                if resizable and not TKToplevel.RESIZABLE[resizable][1]:
                    remove = True
            if remove:
                kw.pop(key)
            else:
                self._h_set = True
        key = "menu"
        if key in kw:
            # No menu preview available
            kw.pop(key)
        return super().configure(cnf, **kw)


class ToplevelPreviewBaseBO(BuilderObject):
    container = True
    container_layout = True
    # Add fake 'modal' property for Dialog preview
    properties = TKToplevel.properties + ("modal",)
    ro_properties = TKToplevel.ro_properties

    def configure(self, target=None):
        # setup width and height properties if
        # geometry is defined.
        geom = "geometry"
        if geom in self.wmeta.properties:
            w, h = self._get_dimwh(self.wmeta.properties[geom])
            if w and h:
                self.wmeta.properties["width"] = w
                self.wmeta.properties["height"] = h
        super().configure(target)

    def configure_children(self, target=None):
        w = self.widget
        # Set a fixed size in preview if geometry is set.
        if "geometry" in self.wmeta.properties:
            if w.pack_slaves():
                w.pack_propagate(0)
            elif w.grid_slaves():
                w.grid_propagate(0)

    def layout(self, target=None):
        self.widget.pack(expand=True, fill="both")
        self._container_layout(
            self.widget,
            self.wmeta.container_manager,
            self.wmeta.container_properties,
        )

    def _get_dimwh(self, dimvalue: str):
        # get width and height from dimension string
        dim = dimvalue.split("+")[0]
        dim = dim.split("-")[0]
        w, h = dim.split("x")
        return (w, h)

    def _set_property(self, target_widget, pname, value):
        tw = target_widget
        tw.tl_attrs[pname] = value
        method_props = (
            "iconbitmap",
            "iconphoto",
            "overrideredirect",
            "title",
        )
        if pname in method_props:
            pass
        elif pname in ("maxsize", "minsize"):
            if not value:
                del tw.tl_attrs[pname]
            elif "|" in value:
                w, h = value.split("|")
                if w and h:
                    tw.tl_attrs[pname] = (int(w), int(h))
                else:
                    del tw.tl_attrs[pname]
        elif pname == "geometry":
            if value:
                w, h = self._get_dimwh(value)
                if w and h:
                    tw.tl_attrs["minsize"] = (int(w), int(h))
                    tw._h_set = tw._w_set = False
                    tw.configure(width=w, height=h)
        elif pname == "resizable":
            # Do nothing, fake 'resizable' property for Toplevel preview
            pass
        elif pname == "modal":
            # Do nothing, fake 'modal' property for dialog preview
            pass
        else:
            super()._set_property(tw, pname, value)
