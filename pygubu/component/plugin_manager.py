import importlib
import pkgutil
import pygubu.plugins

from .plugin_engine import PluginRegistry, BuilderLoaderPlugin


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
            if isinstance(plugin, BuilderLoaderPlugin)
        )
