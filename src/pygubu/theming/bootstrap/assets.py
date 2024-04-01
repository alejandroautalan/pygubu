import tkinter as tk
import math
from ..photodraw import Draw
from .config import (
    PRIMARY,
    SECONDARY,
    SUCCESS,
    INFO,
    WARNING,
    DANGER,
    LIGHT,
    DARK,
    TTK_CLAM,
    TTK_ALT,
    TTK_DEFAULT,
)


class AssetCreator:
    def __init__(self, theme_builder):
        self.builder = theme_builder
        self.theme_images = {}

    @property
    def colors(self):
        return self.builder.colors

    @property
    def colorutil(self):
        return self.builder.colorutil

    @property
    def tk_master(self):
        return self.builder.tk_master

    @property
    def is_light_theme(self):
        return self.builder.is_light_theme

    def create_separator_assets(self, size, color):
        ssize = self.builder.scale_size(size)
        w = ssize[0]
        h = ssize[1]

        draw = Draw(self.tk_master)
        h_img = draw.canvas_new(width=w, height=h)
        draw.rectangle(0, 0, w, h, fill=color)
        v_img = draw.canvas_new(width=h, height=w)
        draw.rectangle(0, 0, h, w, fill=color)
        self.theme_images[h_img.name] = h_img
        self.theme_images[v_img.name] = v_img

        return (h_img.name, v_img.name)

    def create_sizegrip_assets(self, color):
        """Create image assets used to build the sizegrip style.

        Parameters:

            color (str):
                The color _value_ used to draw the image.

        Returns:

            str:
                The PhotoImage name.
        """
        box = self.builder.scale_size(1)
        pad = box * 2
        chunk = box + pad  # 4

        w = chunk * 3 + pad
        h = chunk * 3 + pad

        # size = [w, h]
        draw = Draw(self.tk_master)
        canvas = draw.canvas_new(width=w, height=h)
        draw.rectangle(chunk * 2 + pad, pad, chunk * 3, chunk, fill=color)
        draw.rectangle(
            chunk * 2 + pad, chunk + pad, chunk * 3, chunk * 2, fill=color
        )
        draw.rectangle(
            chunk * 2 + pad,
            chunk * 2 + pad,
            chunk * 3,
            chunk * 3,
            fill=color,
        )
        draw.rectangle(
            chunk + pad, chunk + pad, chunk * 2, chunk * 2, fill=color
        )
        draw.rectangle(
            chunk + pad, chunk * 2 + pad, chunk * 2, chunk * 3, fill=color
        )
        draw.rectangle(pad, chunk * 2 + pad, chunk, chunk * 3, fill=color)
        self.theme_images[canvas.name] = canvas
        return canvas.name

    def create_radiobutton_assets(self, colorname=None):
        """Create the image assets used to build the radiobutton style.

        Parameters:

            colorname (str):

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names
        """
        prime_color = self.colors.get_color(colorname)
        on_fill = prime_color
        off_fill = self.colors.bg
        on_indicator = self.colors.selectfg
        size = self.builder.scale_size([14, 14])

        draw = Draw(self.tk_master)
        off_border = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )
        disabled = self.colorutil.make_transparent(
            0.3, self.colors.fg, self.colors.bg
        )

        if self.is_light_theme:
            if colorname == LIGHT:
                on_indicator = self.colors.dark

        canvas_size = 134
        canvas = draw.canvas_new(width=canvas_size, height=canvas_size)

        # radio off
        x1 = y1 = 1
        x2 = y2 = 133
        stroke = 16
        draw.circle(
            x1, y1, x2, y2, fill=off_fill, outline=off_border, stroke=stroke
        )
        scale_factor = size[0] / canvas_size
        off_img = draw.canvas_scale(scale_factor)
        off_name = off_img.name
        self.theme_images[off_name] = off_img

        # radio on
        draw.canvas_blank()
        if colorname == LIGHT and self.is_light_theme:
            draw.circle(x1, y1, x2, y2, outline=off_border, stroke=stroke)
        else:
            draw.circle(x1, y1, x2, y2, fill=on_fill)
        ix1 = iy1 = 40
        ix2 = iy2 = 94
        draw.circle(ix1, iy1, ix2, iy2, fill=on_indicator)
        on_img = draw.canvas_scale(scale_factor)
        on_name = on_img.name
        self.theme_images[on_name] = on_img

        # radio on/disabled
        draw.canvas_blank()
        if colorname == LIGHT and self.is_light_theme:
            draw.circle(x1, y1, x2, y2, outline=off_border, stroke=stroke)
        else:
            draw.circle(x1, y1, x2, y2, fill=disabled)
        draw.circle(ix1, iy1, ix2, iy2, fill=off_fill)
        on_dis_img = draw.canvas_scale(scale_factor)
        on_disabled_name = on_dis_img.name
        self.theme_images[on_disabled_name] = on_dis_img

        # radio disabled
        draw.canvas_blank()
        stroke_3 = 10
        draw.circle(
            x1, y1, x2, y2, outline=disabled, stroke=stroke_3, fill=off_fill
        )
        disabled_img = draw.canvas_scale(scale_factor)
        disabled_name = disabled_img.name
        self.theme_images[disabled_name] = disabled_img
        del canvas

        return off_name, on_name, disabled_name, on_disabled_name

    def create_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create the image assets used to build the standard scrollbar
        style.

        Parameters:

            thumbcolor (str):
                The primary color value used to color the thumb.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        vsize = self.builder.scale_size([9, 28])
        hsize = self.builder.scale_size([28, 9])

        draw = Draw(self.tk_master)

        def create_image(size, color):
            # x = size[0] * 10
            # y = size[1] * 10
            img = draw.canvas_new()
            draw.rectangle(0, 0, size[0], size[1], fill=color)
            self.theme_images[img.name] = img
            return img

        # create images
        h_normal_img = create_image(hsize, thumbcolor)
        h_pressed_img = create_image(hsize, pressed)
        h_active_img = create_image(hsize, active)

        v_normal_img = create_image(vsize, thumbcolor)
        v_pressed_img = create_image(vsize, pressed)
        v_active_img = create_image(vsize, active)

        return (
            h_normal_img,
            h_pressed_img,
            h_active_img,
            v_normal_img,
            v_pressed_img,
            v_active_img,
        )

    def create_scale_assets(self, colorname=None, size=14):
        """Create the assets used for the ttk.Scale widget.

        The slider handle is automatically adjusted to fit the
        screen resolution.

        Parameters:

            colorname (str):
                The color label.

            size (int):
                The size diameter of the slider circle; default=16.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names to be used in the image
                layout when building the style.
        """
        size = self.builder.scale_size(size)
        draw = Draw(self.tk_master)

        if self.is_light_theme:
            disabled_color = self.colors.border
            if colorname == LIGHT:
                track_color = self.colors.bg
            else:
                track_color = self.colors.light
        else:
            disabled_color = self.colors.selectbg
            track_color = self.colorutil.update_hsv(
                self.colors.selectbg, vd=-0.2
            )

        if any([colorname is None, not colorname]):
            normal_color = self.colors.primary
        else:
            normal_color = self.colors.get_color(colorname)

        pressed_color = self.colorutil.update_hsv(normal_color, vd=-0.1)
        hover_color = self.colorutil.update_hsv(normal_color, vd=0.1)

        canvas_size = 100
        scale_factor = size / canvas_size

        # normal state
        canvas = draw.canvas_new(width=canvas_size, height=canvas_size)
        x1 = y1 = 0
        x2 = y2 = 95
        draw.circle(x1, y1, x2, y2, fill=normal_color)
        normal_img = draw.canvas_scale(scale_factor)
        normal_name = normal_img.name
        self.theme_images[normal_name] = normal_img

        # pressed state
        draw.canvas_blank()
        draw.circle(x1, y1, x2, y2, fill=pressed_color)
        pressed_img = draw.canvas_scale(scale_factor)
        pressed_name = pressed_img.name
        self.theme_images[pressed_name] = pressed_img

        # hover state
        draw.canvas_blank()
        draw.circle(x1, y1, x2, y2, fill=hover_color)
        hover_img = draw.canvas_scale(scale_factor)
        hover_name = hover_img.name
        self.theme_images[hover_name] = hover_img

        # disabled state
        draw.canvas_blank()
        draw.circle(x1, y1, x2, y2, fill=disabled_color)
        disabled_img = draw.canvas_scale(scale_factor)
        disabled_name = disabled_img.name
        self.theme_images[disabled_name] = disabled_img
        del canvas

        def create_image(size, color):
            img = draw.canvas_new()
            draw.rectangle(0, 0, size[0], size[1], fill=color)
            self.theme_images[img.name] = img
            return img

        # vertical track ??
        h_track_img = create_image(
            self.builder.scale_size((40, 5)), track_color
        )
        h_track_name = h_track_img.name

        # horizontal track ??
        v_track_img = create_image(
            self.builder.scale_size((5, 40)), track_color
        )
        v_track_name = v_track_img.name

        return (
            normal_name,
            pressed_name,
            hover_name,
            disabled_name,
            h_track_name,
            v_track_name,
        )

    def create_checkbutton_assets(self, colorname=None):
        """Create the image assets used to build the standard
        checkbutton style.

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """

        draw = Draw(self.tk_master)
        prime_color = self.colors.get_color(colorname)
        on_border = prime_color
        on_fill = prime_color
        off_fill = self.colors.bg
        off_border = self.colors.selectbg
        off_border = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )
        disabled_fg = self.colorutil.make_transparent(
            0.3, self.colors.fg, self.colors.bg
        )

        if colorname == LIGHT:
            check_color = self.colors.dark
            on_border = check_color
        elif colorname == DARK:
            check_color = self.colors.light
            on_border = check_color
        else:
            check_color = self.colors.selectfg

        size = self.builder.scale_size([14, 14])

        canvas_size = 134
        scale_factor = size[0] / canvas_size

        # checkbutton off
        canvas = draw.canvas_new(width=canvas_size, height=canvas_size)
        x1 = y1 = 2
        x2 = y2 = 132
        rec_radio = 32
        stroke = 18

        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            fill=off_fill,
            outline=off_border,
            stroke=stroke,
        )
        off_img = draw.canvas_scale(scale_factor)
        off_name = off_img.name
        self.theme_images[off_name] = off_img

        # checkbutton on
        draw.canvas_blank()
        rec_stroke_3 = 10
        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            stroke=rec_stroke_3,
            outline=on_border,
            fill=on_fill,
        )

        shape = [
            [(45, 85), (35, 85), (35, 100), (45, 100)],
            [(48, 87), (66, 60), (82, 60), (63, 87)],
            [(106, 27), (96, 27), (89, 30), (106, 30)],
            [(42, 75), (34, 75), (28, 80), (44, 80)],
            [(44, 80), (28, 80), (30, 90), (49, 90)],
            [(48, 90), (30, 90), (37, 107), (48, 107)],
            [(63, 87), (46, 87), (46, 107), (50, 107)],
            [(66, 60), (89, 30), (106, 30), (82, 60)],
        ]

        for poly in shape:
            draw.convex_poly(poly, check_color)
        # for tri in shape:
        #    draw.triangle_filled(*tri, check_color)

        on_img = draw.canvas_scale(scale_factor)
        on_name = on_img.name
        self.theme_images[on_name] = on_img

        # checkbutton on/disabled
        draw.canvas_blank()
        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            stroke=rec_stroke_3,
            outline=disabled_fg,
            fill=disabled_fg,
        )

        for poly in shape:
            draw.convex_poly(poly, check_color)
        # for tri in shape:
        #     draw.triangle_filled(*tri, off_fill)

        on_dis_img = draw.canvas_scale(scale_factor)
        on_dis_name = on_dis_img.name
        self.theme_images[on_dis_name] = on_dis_img

        # checkbutton alt
        draw.canvas_blank()
        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            stroke=rec_stroke_3,
            outline=on_border,
            fill=on_fill,
        )
        line_coords = [36, 58, 100, 70]
        draw.rectangle(*line_coords, fill=check_color)

        alt_img = draw.canvas_scale(scale_factor)
        alt_name = alt_img.name
        self.theme_images[alt_name] = alt_img

        # checkbutton alt/disabled
        draw.canvas_blank()
        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            stroke=rec_stroke_3,
            outline=disabled_fg,
            fill=disabled_fg,
        )
        draw.rectangle(*line_coords, fill=off_fill)
        alt_dis_img = draw.canvas_scale(scale_factor)
        alt_dis_name = alt_dis_img.name
        self.theme_images[alt_dis_name] = alt_dis_img

        # checkbutton disabled
        draw.canvas_blank()
        draw.rounded_rectangle(
            x1,
            y1,
            x2,
            y2,
            radio=rec_radio,
            stroke=rec_stroke_3,
            outline=disabled_fg,
        )
        disabled_img = draw.canvas_scale(scale_factor)
        disabled_name = disabled_img.name
        self.theme_images[disabled_name] = disabled_img
        del canvas

        return (
            off_name,
            on_name,
            disabled_name,
            alt_name,
            on_dis_name,
            alt_dis_name,
        )

    def create_striped_progressbar_assets(self, thickness, colorname=None):
        """Create the striped progressbar image and return as a
        `PhotoImage`

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A list of photoimage names.
        """
        if any([colorname is None, colorname == ""]):
            barcolor = self.colors.primary
        else:
            barcolor = self.colors.get_color(colorname)

        draw = Draw(self.tk_master)
        # calculate value of the light color
        brightness = self.colorutil.rgb_to_hsv(
            *self.colorutil.hex_to_rgb(barcolor)
        )[2]
        if brightness < 0.4:
            value_delta = 0.3
        elif brightness > 0.8:
            value_delta = 0
        else:
            value_delta = 0.1

        barcolor_light = self.colorutil.update_hsv(
            barcolor, sd=-0.2, vd=value_delta
        )

        # horizontal progressbar
        canvas_size = 100
        canvas = draw.canvas_new(width=canvas_size, height=canvas_size)
        draw.rectangle(0, 0, 100, 100, fill=barcolor_light)
        shape = [(0, 0), (48, 0), (100, 52), (100, 100)]
        draw.convex_poly(shape, barcolor)
        shape = [(0, 52), (48, 100), (0, 100)]
        draw.convex_poly(shape, barcolor)

        scale_factor = thickness / canvas_size
        h_img = draw.canvas_scale(scale_factor)
        h_name = h_img.name

        v_img = h_img.copy()
        v_name = v_img.name
        del canvas
        draw.canvas = v_img
        draw.canvas_rotate(90)

        self.theme_images[h_name] = h_img
        self.theme_images[v_name] = v_img
        return h_name, v_name

    def create_square_toggle_assets(self, colorname=None):
        """Create the image assets used to build a square toggle
        style.

        Parameters:

            colorname (str):
                The color label used to style the widget.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """
        size = self.builder.scale_size([24, 15])
        if any([colorname is None, colorname == ""]):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get_color(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg

        draw = Draw(self.tk_master)

        disabled_fg = self.colorutil.make_transparent(
            0.3, self.colors.fg, self.colors.bg
        )
        off_border = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )
        off_indicator = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

        canvasw = 226
        canvash = 130
        sfw = size[0] / canvasw
        sfh = size[1] / canvash
        stroke6 = 9

        # toggle off
        canvas = draw.canvas_new(width=canvasw, height=canvash)
        draw.rectangle(
            1, 1, 225, 129, outline=off_border, stroke=stroke6, fill=off_fill
        )
        draw.rectangle(20, 20, 110, 110, fill=off_indicator)

        off_img = draw.canvas_scale(sfw, sfh)
        off_name = off_img.name
        self.theme_images[off_name] = off_img

        # toggle on
        draw.canvas_blank()
        draw.rectangle(
            1, 1, 225, 129, outline=on_border, stroke=stroke6, fill=on_fill
        )
        draw.rectangle(20, 20, 110, 110, fill=on_indicator)
        draw.canvas_rotate(180)
        on_img = draw.canvas_scale(sfw, sfh)
        on_name = on_img.name
        self.theme_images[on_name] = on_img

        # toggle disabled
        draw.canvas_blank()
        draw.rectangle(1, 1, 225, 129, outline=disabled_fg, stroke=stroke6)
        draw.rectangle(20, 20, 110, 110, fill=disabled_fg)
        disabled_img = draw.canvas_scale(sfw, sfh)
        disabled_name = disabled_img.name
        self.theme_images[disabled_name] = disabled_img

        # toggle on / disabled
        draw.canvas_blank()
        draw.rectangle(
            1, 1, 225, 129, outline=disabled_fg, stroke=stroke6, fill=off_fill
        )
        draw.rectangle(20, 20, 110, 110, fill=disabled_fg)
        draw.canvas_rotate(180)
        on_dis_img = draw.canvas_scale(sfw, sfh)
        on_disabled_name = on_dis_img.name
        self.theme_images[on_disabled_name] = on_dis_img

        del canvas
        return off_name, on_name, disabled_name, on_disabled_name

    def create_round_toggle_assets(self, colorname=None):
        """Create image assets for the round toggle style.

        Parameters:

            colorname (str):
                The color label assigned to the colors property.

        Returns:

            Tuple[str]:
                A tuple of PhotoImage names.
        """
        size = self.builder.scale_size([24, 15])

        if any([colorname is None, colorname == ""]):
            colorname = PRIMARY

        # set default style color values
        prime_color = self.colors.get_color(colorname)
        on_border = prime_color
        on_indicator = self.colors.selectfg
        on_fill = prime_color
        off_fill = self.colors.bg

        draw = Draw(self.tk_master)

        disabled_fg = self.colorutil.make_transparent(
            0.3, self.colors.fg, self.colors.bg
        )
        off_border = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )
        off_indicator = self.colorutil.make_transparent(
            0.4, self.colors.fg, self.colors.bg
        )

        # override defaults for light and dark colors
        if colorname == LIGHT:
            on_border = self.colors.dark
            on_indicator = on_border
        elif colorname == DARK:
            on_border = self.colors.light
            on_indicator = on_border

        # specific
        canvasw = 226
        canvash = 130
        sfw = size[0] / canvasw
        sfh = size[1] / canvash
        stroke6 = 9
        radius = int(128 / 2)

        # toggle off
        rec_coords = (1, 1, 225, 129)
        ellip_coords = (20, 18, 112, 110)
        canvas = draw.canvas_new(width=canvasw, height=canvash)
        draw.rounded_rectangle(
            *rec_coords,
            radio=radius,
            outline=off_border,
            stroke=stroke6,
            fill=off_fill,
        )
        draw.circle(*ellip_coords, fill=off_indicator)

        off_img = draw.canvas_scale(sfw, sfh)
        off_name = off_img.name
        self.theme_images[off_name] = off_img

        # toggle on
        draw.canvas_blank()
        draw.rounded_rectangle(
            *rec_coords,
            radio=radius,
            outline=on_border,
            stroke=stroke6,
            fill=on_fill,
        )
        draw.circle(*ellip_coords, fill=on_indicator)
        draw.canvas_rotate(180)

        on_img = draw.canvas_scale(sfw, sfh)
        on_name = on_img.name
        self.theme_images[on_name] = on_img

        # toggle on / disabled
        draw.canvas_blank()
        draw.rounded_rectangle(
            *rec_coords,
            radio=radius,
            outline=disabled_fg,
            stroke=stroke6,
            fill=off_fill,
        )
        draw.circle(*ellip_coords, fill=disabled_fg)
        draw.canvas_rotate(180)

        on_dis_img = draw.canvas_scale(sfw, sfh)
        on_disabled_name = on_dis_img.name
        self.theme_images[on_disabled_name] = on_dis_img

        # toggle disabled
        draw.canvas_blank()
        draw.rounded_rectangle(
            *rec_coords, radio=radius, outline=disabled_fg, stroke=stroke6
        )
        draw.circle(*ellip_coords, fill=disabled_fg)

        disabled_img = draw.canvas_scale(sfw, sfh)
        disabled_name = disabled_img.name
        self.theme_images[disabled_name] = disabled_img
        del canvas
        return off_name, on_name, disabled_name, on_disabled_name

    def create_round_scrollbar_assets(self, thumbcolor, pressed, active):
        """Create image assets to be used when building the round
        scrollbar style.

        Parameters:

            thumbcolor (str):
                The color value of the thumb in normal state.

            pressed (str):
                The color value to use when the thumb is pressed.

            active (str):
                The color value to use when the thumb is active or
                hovered.
        """
        vsize = self.builder.scale_size([9, 28])
        hsize = self.builder.scale_size([28, 9])

        draw_v = Draw(self.tk_master)
        vw = vsize[0] * 10
        vh = vsize[1] * 10
        vsfw = vsize[0] / vw
        vsfh = vsize[1] / vh
        vradius = min([vw, vh]) // 2
        draw_v.canvas_new(width=vw, height=vh)

        hw = hsize[0]
        hh = hsize[1]
        hsfw = hsize[0] / hw
        hsfh = hsize[1] / hh
        hradius = min([hw, hh]) // 2
        draw_h = Draw(self.tk_master)
        draw_h.canvas_new(width=hsize[0], height=hsize[1])

        def vrounded_rect(color):
            draw_v.canvas_blank()
            draw_v.rounded_rectangle(
                0, 0, vw - 1, vh - 1, radio=vradius, fill=color
            )
            img = draw_v.canvas_scale(vsfw, vsfh)
            self.theme_images[img.name] = img
            return img.name

        def hrounded_rect(color):
            draw_h.canvas_blank()
            draw_h.rounded_rectangle(
                0, 0, hw - 1, hh - 1, radio=hradius, fill=color
            )
            img = draw_h.canvas_scale(hsfw, hsfh)
            self.theme_images[img.name] = img
            return img.name

        # create images
        h_normal_img = hrounded_rect(thumbcolor)
        h_pressed_img = hrounded_rect(pressed)
        h_active_img = hrounded_rect(active)

        v_normal_img = vrounded_rect(thumbcolor)
        v_pressed_img = vrounded_rect(pressed)
        v_active_img = vrounded_rect(active)

        del draw_h.canvas
        del draw_v.canvas

        return (
            h_normal_img,
            h_pressed_img,
            h_active_img,
            v_normal_img,
            v_pressed_img,
            v_active_img,
        )
