import math
import time
import tkinter as tk


class TkPhotoDraw:
    """A fallback class for drawing in a tk.PhotoImage."""

    def __init__(self, master):
        self.tk_master: tk.Widget = master
        self.canvas: tk.PhotoImage = None

    def _tk_call(self, *args, **kw):
        return self.tk_master.tk.call(*args, **kw)

    # Canvas related functions begin
    def canvas_new(self, **photo_args):
        if "master" not in photo_args:
            photo_args["master"] = self.tk_master
        self.canvas = tk.PhotoImage(**photo_args)
        return self.canvas

    def canvas_blank(self):
        self.canvas.blank()

    def canvas_scale(self, xf, yf=0) -> tk.PhotoImage:
        """Scale canvas to new image.
        Returns:
           tk.PhotoImage
        """
        mode = "-subsample"
        if abs(xf) < 1:
            xf = 1.0 / xf
            if abs(yf) < 1 and yf != 0:
                yf = 1.0 / yf
        elif xf >= 0 and yf >= 0:
            mode = "-zoom"
        if yf == 0:
            yf = xf
        xf, yf = int(xf), int(yf)
        tmp = tk.PhotoImage(master=self.tk_master)
        self.tk_master.tk.call(
            tmp.name, "copy", self.canvas.name, "-shrink", mode, xf, yf
        )
        return tmp

    def canvas_rotate(self, angle: int, bg_color=None):
        if bg_color is None:
            bg_color = "#000000"
        w = self.canvas.width()
        h = self.canvas.height()
        tmp = self.canvas.copy()
        self.canvas.blank()
        if angle == 180 or angle == -180:
            self._tk_call(
                self.canvas.name, "copy", tmp.name, "-subsample", -1, -1
            )
        elif angle == 90:
            self._rotate_90(bg_color, w, h, tmp)
        elif angle == -90 or angle == 270:
            self._rotate_270(bg_color, w, h, tmp)
        else:
            self._handle_other_rotations(angle, bg_color, w, h, tmp)
        del tmp

    def _handle_other_rotations(self, angle, bg_color, w, h, tmp):
        buf = []
        alpha = []
        bg_rgb = self.tk_master.winfo_rgb(bg_color)
        a = math.atan(1) * 8 * angle / 360
        xm = w / 2
        ym = h / 2
        w2 = round(abs(w * math.cos(a)) + abs(h * math.sin(a)))
        xm2 = w2 / 2
        h2 = round(abs(h * math.cos(a)) + abs(w * math.sin(a)))
        ym2 = h2 / 2
        self.canvas.config(width=w2, height=h2)
        for i in range(0, h2):
            to_x = -1
            for j in range(0, w2):
                rad = math.hypot(ym2 - i, xm2 - j)
                th = math.atan2(ym2 - i, xm2 - j) + a
                x = xm - rad * math.cos(th)
                if x < 0 or x >= w:
                    alpha.append((i, j))
                    continue
                y = ym - rad * math.sin(th)
                if y < 0 or y >= h:
                    alpha.append((i, j))
                    continue
                x0 = int(x)
                x1 = x0 + 1 if (x0 + 1) < w else x0
                dx = x1 - x
                y0 = int(y)
                y1 = y0 + 1 if (y0 + 1) < h else y0
                dy = y1 - y
                R = G = B = 0

                rgb1 = tmp.get(x0, y0)
                rgb2 = tmp.get(x0, y1)
                rgb3 = tmp.get(x1, y0)
                rgb4 = tmp.get(x1, y1)

                if (
                        rgb1 == bg_rgb
                        or rgb2 == bg_rgb
                        or rgb3 == bg_rgb
                        or rgb4 == bg_rgb
                    ):
                    alpha.append((i, j))
                else:
                    r, g, b = rgb1
                    R = R + r * dx * dy
                    G = G + g * dx * dy
                    B = B + b * dx * dy
                    r, g, b = rgb2
                    R = R + r * dx * (1 - dy)
                    G = G + g * dx * (1 - dy)
                    B = B + b * dx * (1 - dy)
                    r, g, b = rgb3
                    R = R + r * (1 - dx) * dy
                    G = G + g * (1 - dx) * dy
                    B = B + b * (1 - dx) * dy
                    r, g, b = rgb4
                    R = R + r * (1 - dx) * (1 - dy)
                    G = G + g * (1 - dx) * (1 - dy)
                    B = B + b * (1 - dx) * (1 - dy)
                rgb = (round(R), round(G), round(B))
                buf.append("#{:02x}{:02x}{:02x}".format(*rgb))
                if to_x == -1:
                    to_x = j
            if to_x >= 0:
                self.canvas.put(buf, to=(i, to_x))
                for x, y in alpha:
                    self.canvas.transparency_set(x, y, True)
                buf.clear()
                alpha.clear()
        del buf

    def _rotate_270(self, bg_color, w, h, tmp):
        bg_rgb = self.tk_master.winfo_rgb(bg_color)
        buf = []
        alpha = []
        for i in range(0, w):
            row = []
            for j in range(h - 1, -1, -1):
                rgb = tmp.get(i, j)
                if rgb == bg_rgb:
                    alpha.append((i, j))
                row.append("#{:02x}{:02x}{:02x}".format(*rgb))
            buf.append(row)
        self.canvas.config(width=h, height=w)
        self.canvas.put(buf)
        for x, y in alpha:
            self.canvas.transparency_set(y, x, True)
        del alpha
        del buf

    def _rotate_90(self, bg_color, w, h, tmp):
        bg_rgb = self.tk_master.winfo_rgb(bg_color)
        buf = []
        alpha = []
        for i in range(w - 1, -1, -1):
            row = []
            for j in range(0, h):
                rgb = tmp.get(i, j)
                if rgb == bg_rgb:
                    alpha.append((i, j))
                row.append("#{:02x}{:02x}{:02x}".format(*rgb))
            buf.append(row)
        self.canvas.config(width=h, height=w)
        self.canvas.put(buf)
        for x, y in alpha:
            self.canvas.transparency_set(y, x, True)
        del alpha
        del buf

    # Canvas related functions end

    @staticmethod
    def bresenham_line(x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        slope = dy > dx
        if slope:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        error = dx // 2
        y = y1
        ystep = 1 if y1 < y2 else -1
        for x in range(x1, x2 + 1):
            coord = (y, x) if slope else (x, y)
            yield coord
            error -= dy
            if error < 0:
                y += ystep
                error += dx

    def _line(self, x1, y1, x2, y2, color):
        """Draw line."""
        for x, y in Draw.bresenham_line(x1, y1, x2, y2):
            self.canvas.put(color, to=(x, y))

    def _draw_rect_filled(self, x1, y1, x2, y2, color):
        # self.canvas.put(color, to=(x1, y1, x2 + 1, y2 + 1))
        self.canvas.put(color, to=(x1, y1, x2, y2))

    def _get_ink(self, fill, outline):
        fill_ink = fill
        border_ink = outline

        if fill is None and outline is None:
            fill_ink = "black"
            border_ink = "black"
        elif fill is None:
            fill_ink = outline
        elif outline is None:
            border_ink = fill_ink
        return fill_ink, border_ink

    def rectangle(self, x1, y1, x2, y2, *, fill=None, outline=None, stroke=1):
        fill_ink, border_ink = self._get_ink(fill, outline)

        if fill_ink == border_ink and fill:
            self._draw_rect_filled(x1, y1, x2, y2, fill_ink)
        else:
            # top line
            self._draw_rect_filled(x1, y1, x2, y1 + stroke, border_ink)
            # bottom
            self._draw_rect_filled(x1, y2 - stroke, x2, y2, border_ink)
            # left
            self._draw_rect_filled(x1, y1, x1 + stroke, y2, border_ink)
            # right
            self._draw_rect_filled(x2 - stroke, y1, x2, y2, border_ink)
            # interior
            if fill:
                self._draw_rect_filled(
                    x1 + stroke, y1 + stroke, x2 - stroke, y2 - stroke, fill_ink
                )

    def rounded_rectangle(
        self, x1, y1, x2, y2, *, fill=None, outline=None, stroke=1, radio=0
    ):
        fill_ink, border_ink = self._get_ink(fill, outline)

        # left border
        self._draw_rect_filled(
            x1, y1 + radio, x1 + stroke, y2 - radio, border_ink
        )
        # right border
        self._draw_rect_filled(
            x2 - stroke, y1 + radio, x2, y2 - radio, border_ink
        )
        # top border
        self._draw_rect_filled(
            x1 + radio, y1, x2 - radio, y1 + stroke, border_ink
        )
        # bottom border
        self._draw_rect_filled(
            x1 + radio, y2 - stroke, x2 - radio, y2, border_ink
        )

        if fill:
            # center rectangle
            self._draw_rect_filled(
                x1 + stroke, y1 + radio, x2 - stroke, y2 - radio, fill_ink
            )
            # top
            self._draw_rect_filled(
                x1 + radio, y1 + stroke, x2 - radio, y1 + radio, fill_ink
            )
            # bottom
            self._draw_rect_filled(
                x1 + radio, y2 - radio, x2 - radio, y2 - stroke, fill_ink
            )

        ix1, iy1, ix2, iy2 = (  # noqa: F841
            x1 + stroke,
            y1 + stroke,
            x2 - stroke,
            y2 - stroke,
        )
        diam = radio * 2
        cx1, cy1, cx2, cy2 = (x1, y1, x2, y2)
        cboxes = (
            (cx1, cy1, cx1 + diam, cy1 + diam, 0),
            (cx2 - diam, cy1, cx2, cy1 + diam, 1),
            (cx1, cy2 - diam, cx1 + diam, cy2, 2),
            (cx2 - diam, cy2 - diam, x2, cy2, 3),
        )
        for cx1, cy1, cx2, cy2, cuadrant in cboxes:
            self.circle_cuadrant(
                cx1,
                cy1,
                cx2,
                cy2,
                cuadrant,
                outline=outline,
                fill=fill,
                stroke=stroke,
            )

    def circle(self, x1, y1, x2, y2, *, fill=None, outline=None, stroke=1):
        d = x2 - x1
        r = int(d / 2)
        # center
        x = x1 + r
        y = y1 + r

        fill_ink, border_ink = self._get_ink(fill, outline)

        # will add +1 to y2 because I'm drawing using
        # filled rectangles from tk photo image

        if fill_ink == border_ink and fill:
            self._draw_rect_filled(x - r, y, x + r, y + 1, fill_ink)
            for i in range(1, r):
                a = int(math.sqrt(r * r - i * i))  # Pythagoras
                self._draw_rect_filled(x - a, y - i, x + a, y - i + 1, fill_ink)
                self._draw_rect_filled(x - a, y + i, x + a, y + i + 1, fill_ink)
        else:
            ix1 = x1 + stroke
            ix2 = x2 - stroke
            dd = ix2 - ix1
            ir = int(dd / 2)
            ix = ix1 + ir
            iy = y1 + stroke + ir

            for i in range(0, r):
                a = r if i == 0 else int(math.sqrt(r * r - i * i))  # Pythagoras
                if i > ir:
                    self._draw_rect_filled(
                        x - a, y - i, x + a, y - i + 1, border_ink
                    )
                    self._draw_rect_filled(
                        x - a, y + i, x + a, y + i + 1, border_ink
                    )
                else:
                    ia = (
                        ir if i == 0 else int(math.sqrt(ir * ir - i * i))
                    )  # Pythagoras
                    x1, y1, x2, y2 = (x - a, y - i, x + a, y - i)
                    ix1, iy1, ix2, iy2 = (ix - ia, iy - i, ix + ia, iy - i)
                    self._draw_rect_filled(x1, y1, ix1, iy1 + 1, border_ink)
                    self._draw_rect_filled(ix2, iy2, x2, y2 + 1, border_ink)
                    if fill:
                        self._draw_rect_filled(ix1, iy1, ix2, iy2 + 1, fill_ink)

                    x1, y1, x2, y2 = (x - a, y + i, x + a, y + i)
                    ix1, iy1, ix2, iy2 = (ix - ia, iy + i, ix + ia, iy + i)
                    self._draw_rect_filled(x1, y1, ix1, iy1 + 1, border_ink)
                    self._draw_rect_filled(ix2, iy2, x2, y2 + 1, border_ink)
                    if fill:
                        self._draw_rect_filled(ix1, iy1, ix2, iy2 + 1, fill_ink)

    def circle_cuadrant(
        self, x1, y1, x2, y2, cuadrant, *, fill=None, outline=None, stroke=1
    ):
        """Draw a circle cuadrant
        Circle cuadrants for this function:
        0 - 1
        2 - 3
        """
        d = x2 - x1
        r = int(d / 2)
        # center
        x = x1 + r
        y = y1 + r

        fill_ink, border_ink = self._get_ink(fill, outline)

        # will add +1 to x2 and y2 because I'm drawing using
        # filled rectangles from tk photo image
        ix1 = x1 + stroke
        ix2 = x2 - stroke
        dd = ix2 - ix1
        ir = int(dd / 2)
        ix = ix1 + ir
        iy = y1 + stroke + ir

        for i in range(0, r):
            a = r if i == 0 else int(math.sqrt(r * r - i * i))  # Pythagoras
            if i > ir:
                # UPPER BORDERS
                if cuadrant == 0:
                    self._draw_rect_filled(
                        x - a, y - i, x, y - i + 1, border_ink
                    )
                    pass
                if cuadrant == 1:
                    self._draw_rect_filled(
                        x, y - i, x + a, y - i + 1, border_ink
                    )
                # BOTTOM BORDERS
                if cuadrant == 2:
                    self._draw_rect_filled(
                        x - a, y + i, x, y + i + 1, border_ink
                    )
                if cuadrant == 3:
                    self._draw_rect_filled(
                        x, y + i, x + a, y + i + 1, border_ink
                    )
            else:
                self._handle_lower_i(cuadrant, fill, x, y, fill_ink, border_ink, ir, ix, iy, i, a)

    def _handle_lower_i(self, cuadrant, fill, x, y, fill_ink, border_ink, ir, ix, iy, i, a):
        ia = (
                    ir if i == 0 else int(math.sqrt(ir * ir - i * i))
                )  # Pythagoras
        x1, y1, x2, y2 = (x - a, y - i, x + a, y - i)
        ix1, iy1, ix2, iy2 = (ix - ia, iy - i, ix + ia, iy - i)
                # upper left
        if 0 == cuadrant:
            self._draw_rect_filled(x1, y1, ix1, iy1 + 1, border_ink)
            if fill:
                self._draw_rect_filled(ix1, iy1, x, iy1 + i, fill_ink)
                # upper right
        if 1 == cuadrant:
            self._draw_rect_filled(ix2, iy2, x2, y2 + 1, border_ink)
            if fill:
                self._draw_rect_filled(x, iy1, ix2, iy2 + 1, fill_ink)

        x1, y1, x2, y2 = (x - a, y + i, x + a, y + i)
        ix1, iy1, ix2, iy2 = (ix - ia, iy + i, ix + ia, iy + i)
                # bottom left
        if 2 == cuadrant:
            self._draw_rect_filled(x1, y1, ix1, iy1 + 1, border_ink)
            if fill:
                self._draw_rect_filled(ix1, iy1, x, iy2 + 1, fill_ink)
                # bottom right
        if 3 == cuadrant:
            self._draw_rect_filled(ix2, iy2, x2, y2 + 1, border_ink)
            if fill:
                self._draw_rect_filled(x, iy1, ix2, iy2 + 1, fill_ink)

    def triangle(self, x1, y1, x2, y2, x3, y3, color):
        self._line(x1, y1, x2, y2, color)
        self._line(x2, y2, x3, y3, color)
        self._line(x3, y3, x1, y1, color)

    def triangle_filled(self, x1, y1, x2, y2, x3, y3, color):
        x1, y1, x2, y2, x3, y3 = self._sort_verticesby_y(x1, y1, x2, y2, x3, y3)
        if y2 == y3:
            self._fill_bottom_flat_tri(x1, y1, x2, y2, x3, y3, color)
        elif y1 == y2:
            self._fill_top_flat_tri(x1, y1, x2, y2, x3, y3, color)
        else:
            newx = int(x1 + ((y2 - y1) / (y3 - y1)) * (x3 - x1))
            newy = y2
            self._fill_bottom_flat_tri(x1, y1, x2, y2, newx, newy, color)
            self._fill_top_flat_tri(x2, y2, newx, newy, x3, y3, color)

    def _fill_bottom_flat_tri(self, x1, y1, x2, y2, x3, y3, color):
        slope1 = (x2 - x1) / (y2 - y1)
        slope2 = (x3 - x1) / (y3 - y1)
        hx1 = x1
        hx2 = x1 + 0.5
        for scanline_y in range(y1, y2):
            self._draw_rect_filled(
                int(hx1), scanline_y, int(hx2), scanline_y + 1, color
            )
            hx1 += slope1
            hx2 += slope2

    def _fill_top_flat_tri(self, x1, y1, x2, y2, x3, y3, color):
        slope1 = (x3 - x1) / (y3 - y1)
        slope2 = (x3 - x2) / (y3 - y2)
        hx1 = x3
        hx2 = x3 + 0.5
        for scanline_y in range(y3, y1 - 1, -1):
            self._draw_rect_filled(
                int(hx1), scanline_y, int(hx2), scanline_y + 1, color
            )
            hx1 -= slope1
            hx2 -= slope2

    def _sort_verticesby_y(self, x1, y1, x2, y2, x3, y3):
        verts = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda x: x[1])
        return (p for v in verts for p in v)

    def convex_poly(self, points, color):
        if self.is_convex(points):
            # points = sorted(points, key=lambda x: x[1])
            for t in self._tripoly(points):
                self.triangle_filled(*t[0], *t[1], *t[2], color)
        else:
            raise Exception("Not a convex polygon.")

    def _cross_prod(self, points):
        # A[0][0]  px1 [0][1]  py1
        # A[1][0]  px2 A[1][1]  py2
        # A[2][0]  px3 A[2][1]  py3

        x1 = points[1][0] - points[0][0]
        y1 = points[1][1] - points[0][1]
        x2 = points[2][0] - points[0][0]
        y2 = points[2][1] - points[0][1]
        # Return cross product
        return x1 * y2 - y1 * x2

    def _tripoly(self, poly):
        return [(poly[0], b, c) for b, c in zip(poly[1:], poly[2:])]

    def is_convex(self, points):
        # Stores count of
        # edges in polygon
        N = len(points)
        # Stores direction of cross product
        # of previous traversed edges
        prev = 0
        # Stores direction of cross product
        # of current traversed edges
        curr = 0
        # Traverse the array
        for i in range(N):
            # Stores three adjacent edges
            # of the polygon
            temp = (points[i], points[(i + 1) % N], points[(i + 2) % N])
            # Update curr
            curr = self._cross_prod(temp)
            # If curr is not equal to 0
            if curr != 0:
                # If direction of cross product of
                # all adjacent edges are not same
                if curr * prev < 0:
                    return False
                else:
                    # Update curr
                    prev = curr

        return True


Draw = TkPhotoDraw


if __name__ == "__main__":
    root = tk.Tk()
    root.imgs = []

    draw = Draw(root)
    # rectangle
    rr = draw.canvas_new(width=300, height=100)
    root.imgs.append(rr)
    draw.rectangle(10, 10, 90, 90, outline="green", stroke=1)
    draw.rectangle(110, 10, 190, 90, fill="lightgreen")
    draw.rectangle(
        210, 10, 290, 90, fill="lightgreen", outline="green", stroke=10
    )
    label = tk.Label(root, image=rr)
    label.pack()

    # rounded rectangle
    rr = draw.canvas_new(width=300, height=100)
    root.imgs.append(rr)
    draw.rounded_rectangle(10, 10, 90, 90, radio=20, outline="green", stroke=1)
    draw.rounded_rectangle(110, 10, 190, 90, radio=20, fill="lightgreen")
    draw.rounded_rectangle(
        210,
        10,
        290,
        90,
        radio=20,
        fill="lightgreen",
        outline="green",
        stroke=10,
    )
    label = tk.Label(root, image=rr)
    label.pack()

    # circle cuadrant
    rr = draw.canvas_new(width=300, height=100)
    root.imgs.append(rr)
    draw.circle_cuadrant(10, 10, 90, 90, 3, outline="green")
    draw.circle_cuadrant(110, 10, 190, 90, 3, fill="lightgreen")
    draw.circle_cuadrant(
        210, 10, 290, 90, 3, fill="lightgreen", outline="green", stroke=10
    )
    label = tk.Label(root, image=rr)
    label.pack()

    # circle
    rr = draw.canvas_new(width=300, height=100)
    root.imgs.append(rr)
    draw.circle(10, 10, 90, 90, outline="green")
    draw.circle(110, 10, 190, 90, fill="lightgreen")
    draw.circle(210, 10, 290, 90, fill="lightgreen", outline="green", stroke=10)
    label = tk.Label(root, image=rr)
    label.pack()

    # triangle
    rr = draw.canvas_new(width=300, height=100)
    root.imgs.append(rr)
    draw.triangle(10, 90, 50, 0, 90, 90, "green")
    # triangle filled
    draw.triangle_filled(110, 90, 150, 0, 190, 90, "green")
    draw.triangle_filled(210, 0, 290, 0, 250, 90, "green")
    label = tk.Label(root, image=rr)
    label.pack()

    # shape
    rr = draw.canvas_new(width=134, height=134)
    root.imgs.append(rr)
    shape = [
        (34, 76, 38, 72, 43, 70),
        (35, 77, 38, 88, 43, 98),
        (34, 76, 52, 82, 44, 100),
        (34, 76, 51, 82, 44, 70),
        (43, 100, 51, 82, 53, 98),
        (51, 82, 53, 98, 64, 82),
        (52, 81, 64, 82, 85, 53),
        (52, 81, 85, 53, 71, 53),
        (85, 53, 71, 53, 100, 34),
        (71, 53, 100, 34, 85, 35),
        (100, 34, 85, 35, 96, 30),
        (85, 35, 90, 31, 97, 30),
        (96, 30, 100, 34, 101, 30),
    ]
    for x1, y1, x2, y2, x3, y3 in shape:
        draw.triangle_filled(x1, y1, x2, y2, x3, y3, "brown")
    label = tk.Label(root, image=rr)
    label.pack()

    points = [[0, 0], [0, 10], [10, 10], [10, 0]]
    points2 = [(0, 0), (0, 10), (5, 5), (10, 10), (10, 0)]

    for p in (points, points2):
        if draw.is_convex(p):
            print("Yes")
            draw.convex_poly(p, "red")
        else:
            print("No")

    root.mainloop()
