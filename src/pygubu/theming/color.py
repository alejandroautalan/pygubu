import colorsys
import tkinter as tk


class ColorUtil:
    """Color utilities using tkinter functions."""

    def __init__(self, master):
        self.tk_master: tk.Widget = master

    # Color utilities begin
    def make_transparent(self, alpha, foreground, background="#ffffff"):
        """Simulate color transparency."""
        fg = tuple((c // 256 for c in self.tk_master.winfo_rgb(foreground)))
        bg = tuple((c // 256 for c in self.tk_master.winfo_rgb(background)))
        rgb_float = [alpha * c1 + (1 - alpha) * c2 for (c1, c2) in zip(fg, bg)]
        rgb_int = [int(x) for x in rgb_float]
        return "#{:02x}{:02x}{:02x}".format(*rgb_int)

    def hex_to_rgb(self, color: str):
        return tuple((c // 256 for c in self.tk_master.winfo_rgb(color)))

    def update_hsv(self, color, hd=0, sd=0, vd=0):
        """Modify the hue, saturation, and/or value of a given hex
        color value by specifying the _delta_.

        Parameters:

            color (str):
                A hexadecimal color value to adjust.

            hd (float):
                % change in hue, _hue delta_.

            sd (float):
                % change in saturation, _saturation delta_.

            vd (float):
                % change in value, _value delta_.

        Returns:

            str:
                The resulting hexadecimal color value
        """
        rgb_256 = tuple((c // 256 for c in self.tk_master.winfo_rgb(color)))
        r, g, b = tuple((c / 256 for c in rgb_256))
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        # hue
        if h * (1 + hd) > 1:
            h = 1
        elif h * (1 + hd) < 0:
            h = 0
        else:
            h *= 1 + hd
        # saturation
        if s * (1 + sd) > 1:
            s = 1
        elif s * (1 + sd) < 0:
            s = 0
        else:
            s *= 1 + sd
        # value
        if v * (1 + vd) > 1:
            v = 0.95
        elif v * (1 + vd) < 0.05:
            v = 0.05
        else:
            v *= 1 + vd

        rgb_float = colorsys.hsv_to_rgb(h, s, v)
        rgb_int = [int(x * 256) for x in rgb_float]
        return "#{:02x}{:02x}{:02x}".format(*rgb_int)

    def rgb_to_hsv(self, r, g, b):
        """Convert an rgb to hsv color value.

        Parameters:
            r (float):
                red
            g (float):
                green
            b (float):
                blue

        Returns:
            Tuple[float, float, float]: The hsv color value.
        """
        return colorsys.rgb_to_hsv(r, g, b)

    # Color utilities end
