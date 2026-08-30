import sys
import importlib
import pkgutil
import logging
import pygubu.plugins

from typing import List
from .plugin_engine import PluginRegistry, IBuilderLoaderPlugin, IDesignerPlugin

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

logger = logging.getLogger(__name__)


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
        # Discover all plugins
        for _, name, _ in iter_namespace(pygubu.plugins):
            importlib.import_module(name)

        discovered_plugins = entry_points(group="pygubu.plugins")
        for plugin_module in discovered_plugins:
            plugin_module.load()

        # Sorting
        ordered_plugin_classes = cls._get_ordered_plugins()

        # Instanciación y Activación con control de fallas en cascada
        activated_instances = []
        # Diccionario para rastrear la salud de cada plugin por su ID: True (Ok), False (Falló)
        plugins_health = {}

        for plugin_cls in ordered_plugin_classes:
            plugin_id = plugin_cls.get_uid()
            dependencies = plugin_cls.get_dependencies()

            # Validar si alguna de sus dependencias previas falló o no se cargó
            dependency_failed = False
            for dep_id in dependencies:
                if not plugins_health.get(
                    dep_id, False
                ):  # Si es False o no existe en el registro exitoso
                    logger.warning(
                        f"Skipping activation of '{plugin_id}': Dependency '{dep_id}' is not active or failed."
                    )
                    dependency_failed = True
                    break

            if dependency_failed:
                plugins_health[plugin_id] = (
                    False  # Se marca como fallido por arrastre
                )
                continue

            # Intentar activar el plugin actual
            try:
                instance = plugin_cls()
                is_operational = instance.do_activate()

                if is_operational:
                    plugins_health[plugin_id] = True
                    activated_instances.append(instance)
                    logger.info(f"Plugin '{plugin_id}' successfully activated.")
                else:
                    plugins_health[plugin_id] = False
                    logger.info(
                        f"The plugin '{plugin_id}' returned False in do_activate()."
                    )

            except Exception as e:
                plugins_health[plugin_id] = False
                logger.error(
                    f"Critical exception when activating plugin '{plugin_id}': {e}",
                    exc_info=True,
                )

        cls.plugins.extend(activated_instances)

    @classmethod
    def _get_ordered_plugins(cls) -> List:
        """Return a list of plugins sorted by dependency."""
        # Map by UID
        registry_dict = {
            plugin_cls.get_uid(): plugin_cls
            for plugin_cls in PluginRegistry.plugins
        }
        visited = {}
        ordered_plugin_classes = []

        def visit(plugin_cls):
            plugin_id = plugin_cls.get_uid()
            if visited.get(plugin_id) == "visiting":
                raise RuntimeError(
                    f"Circular dependency detected in the plugin: {plugin_id}!"
                )

            if plugin_id not in visited:
                visited[plugin_id] = "visiting"
                for dep_id in plugin_cls.get_dependencies():
                    dep_cls = registry_dict.get(dep_id)
                    if dep_cls:
                        visit(dep_cls)
                    else:
                        # Si falta la dependencia en el entorno, lo marcamos para no intentar nada
                        raise ValueError(
                            f"The plugin '{plugin_id}' depends on '{dep_id}', but it is not installed."
                        )

                visited[plugin_id] = "visited"
                ordered_plugin_classes.append(plugin_cls)

        # Ordenar las clases detectadas
        for plugin in PluginRegistry.plugins:
            try:
                visit(plugin)
            except (RuntimeError, ValueError) as e:
                logger.error(f"Error resolving dependencies: {e}")
                # Eliminamos el plugin problemático para que no intente activarse
                if plugin in ordered_plugin_classes:
                    ordered_plugin_classes.remove(plugin)
        return ordered_plugin_classes

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

    @classmethod
    def is_toplevel_widget(cls, builder_uid: str) -> bool:
        is_toplevel = False
        for plugin in cls.designer_plugins:
            is_toplevel = plugin.is_toplevel_widget(builder_uid)
            if is_toplevel:
                break
        return is_toplevel
