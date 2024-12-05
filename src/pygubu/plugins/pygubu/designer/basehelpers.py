import tkinter as tk
from pygubu.api.v1 import BuilderObject
from pygubu.plugins.tk.tkstdwidgets import TKToplevel


class ToplevelPreviewFactory(type):
    def __new__(cls, clsname, superclasses, attrs):
        return type.__new__(cls, str(clsname), superclasses, attrs)


class ToplevelPreviewMixin(object):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.tl_attrs = {}
        self._w_set = False  # Marks if width was set using "width" property
        self._h_set = False  # Marks if height was set using "height" property
        self._propagate = True  # Save propagate state configured by user
        self._geometry_set = False
        self._geom_w = 1
        self._geom_h = 1
        self._uwidth = 1  # Save width configured by user
        self._uheight = 1  # Save height configured by user

    def _get_req_wh(self):
        """Calculate aproximation of real width and height
        because this frame is locked for preview purposes."""
        my_w = self._uwidth
        my_h = self._uheight
        has_minsize = False
        min_w = my_w
        min_h = my_h
        final_w = my_w
        final_h = my_h

        if "minsize" in self.tl_attrs:
            minsize = self.tl_attrs.get("minsize", (1, 1))
            min_w = minsize[0]
            min_h = minsize[1]
            has_minsize = True

        content_w = content_h = 0
        if self._propagate:
            content_w = super().winfo_reqwidth()
            content_h = super().winfo_reqheight()
            children = self.winfo_children()
            if children:
                if has_minsize:
                    # propagate is enabled, resize to
                    # content size or minsize
                    final_w = max(content_w, min_w)
                    final_h = max(content_h, min_h)
                else:
                    final_w = content_w
                    final_h = content_h
            else:
                # No children, show frame with user configured size
                final_w = max(my_w, min_w)
                final_h = max(my_h, min_h)
        else:
            # Propagate is false, fixed w/h frame.
            final_w = max(min_w, my_w)
            final_h = max(min_h, my_h)
        if self._geometry_set:
            # Geometry overrides all
            final_w = self._geom_w
            final_h = self._geom_h
        # print(f"{my_w=}, {my_h=}, {has_minsize=}, {min_w=}, {min_h=}, {content_w=}, {content_h=}")
        # print(f"{final_w=}, {final_h=}")
        return (final_w, final_h)

    def winfo_reqwidth(self):
        return self._get_req_wh()[0]

    def winfo_reqheight(self):
        return self._get_req_wh()[1]

    def configure(self, cnf=None, **kw):
        if cnf:
            return super().configure(cnf, **kw)
        self._handle_width(kw)
        self._handle_height(kw)
        key = "menu"
        if key in kw:
            # No menu preview available
            kw.pop(key)
        return super().configure(cnf, **kw)

    def _handle_height(self, kw):
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
            # save user height setting
            self._uheight = value

    def _handle_width(self, kw):
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
            # save user width setting
            self._uwidth = value


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

    def _container_layout(self, target, container_manager, properties):
        # save user configured propagate state
        value = self.wmeta.container_properties.get("propagate", True)
        value = self._process_property_value("propagate", value)
        self.widget._propagate = value
        super()._container_layout(target, container_manager, properties)

    def layout(self, target=None, *, forget=False):
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
        return (int(w), int(h))

    def _process_property_value(self, pname, value):
        if pname in ("maxsize", "minsize"):
            if "|" in value:
                w, h = value.split("|")
                value = (int(w), int(h))
            return value
        if pname == "propagate":
            return tk.getboolean(value)
        return super()._process_property_value(pname, value)

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
            pvalue = self._process_property_value(pname, value)
            if not pvalue:
                del tw.tl_attrs[pname]
            else:
                if isinstance(pvalue, tuple):
                    tw.tl_attrs[pname] = pvalue
                    if pname == "minsize":
                        tw.configure(width=pvalue[0], height=pvalue[1])
                else:
                    del tw.tl_attrs[pname]
        elif pname == "geometry":
            self._handle_geometry(value, tw)
        elif pname == "resizable":
            # Do nothing, fake 'resizable' property for Toplevel preview
            pass
        elif pname == "modal":
            # Do nothing, fake 'modal' property for dialog preview
            pass
        elif pname in ("className", "baseName"):
            # Do nothing, fake properties for dialog preview
            pass
        else:
            super()._set_property(tw, pname, value)

    def _handle_geometry(self, value, tw):
        if value:
            w, h = self._get_dimwh(value)
            if w and h:
                w, h = int(w), int(h)
                tw.tl_attrs["minsize"] = (w, h)
                tw._h_set = tw._w_set = False
                tw.configure(width=w, height=h)
                tw._geometry_set = True
                tw._geom_w = w
                tw._geom_h = h
