import importlib
import pkgutil
import pygubu.plugins

from .plugin_engine import PluginRegistry, IBuilderLoaderPlugin, IDesignerPlugin


def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    #
    # Source: https://packaging.python.org/guides/creating-and-discovering-plugins/
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


class PluginManager:
    plugins = []
    designer_plugins = []

    @classmethod
    def load_plugins(cls):
        for _, name, _ in iter_namespace(pygubu.plugins):
            importlib.import_module(name)

        for class_ in PluginRegistry.plugins:
            plugin = class_()
            if plugin.do_activate():
                cls.plugins.append(plugin)

    @classmethod
    def builder_plugins(cls):
        return (
            plugin
            for plugin in cls.plugins
            if isinstance(plugin, IBuilderLoaderPlugin)
        )

    @classmethod
    def load_designer_plugins(cls):
        for plugin in cls.plugins:
            helper = plugin.get_designer_plugin()
            if helper:
                cls.designer_plugins.append(helper)

    @classmethod
    def get_preview_builder_for(cls, builder_uid: str):
        builder = None
        for plugin in cls.designer_plugins:
            builder = plugin.get_preview_builder(builder_uid)
            if builder is not None:
                break
        return builder

    @classmethod
    def get_toplevel_preview_for(
        cls, builder_uid, widget_id, builder, top_master
    ):
        top_preview = None
        for plugin in cls.designer_plugins:
            top_preview = plugin.get_toplevel_preview_for(
                builder_uid, widget_id, builder, top_master
            )
            if top_preview is not None:
                break
        return top_preview

    @classmethod
    def configure_for_preview(cls, builder_uid: str, target):
        for plugin in cls.designer_plugins:
            plugin.configure_for_preview(builder_uid, target)

    @classmethod
    def ensure_visibility_in_preview(cls, builder, selected_uid: str):
        for plugin in cls.designer_plugins:
            plugin.ensure_visibility_in_preview(builder, selected_uid)
