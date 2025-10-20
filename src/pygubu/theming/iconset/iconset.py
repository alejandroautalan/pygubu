class IconSet:
    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    def __init__(self, iconset_definition: dict):
        self.data = iconset_definition

    @property
    def light_color(self):
        return self.data.get("default_light_color", "#ffffff")

    @property
    def dark_color(self):
        return self.data.get("default_dark_color", "#000000")

    @property
    def icon_size(self):
        return self.data.get("default_size", 24)

    @property
    def with_png(self):
        return self.data.get("with_png", False)

    @property
    def with_gif(self):
        return self.data.get("with_gif", False)

    def __contains__(self, item):
        return item in self.data["icons"]

    def icon_props(self, uid, theme=None):
        theme = type(self).THEME_LIGHT if theme is None else theme
        icons = self.data["icons"]
        if uid in icons:
            size = icons[uid].get("size", self.icon_size)
            fn = icons[uid].get("fn", uid)
            color_override = icons[uid].get("color_override", True)
            color = icons[uid].get("light_color", self.light_color)
            if theme == type(self).THEME_DARK:
                color = icons[uid].get("dark_color", self.dark_color)
            return (fn, size, color_override, color)
        return (None, None, None, None)
