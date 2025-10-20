import tkinter as tk


class PhotoResizer:
    """A photo scaler class implemented with zoom and subsample operations."""

    def image_resize(
        self,
        simg: tk.PhotoImage,
        target_w: int,
        target_h: int = None,
        tk_photo_class=None,
    ):
        tk_photo_class = (
            tk.PhotoImage if tk_photo_class is None else tk_photo_class
        )
        target_h = target_w if target_h is None else target_h
        source_w = simg.width()
        source_h = simg.height()

        result_image = tk_photo_class(
            master=simg.tk, width=target_w, height=target_h
        )
        operations = list()
        if target_w < source_w and target_h < source_h:
            # reduce
            self.img_reduce(source_w, source_h, target_w, target_h, operations)
        elif target_w > source_w and target_h > source_h:
            # enlarge
            self.img_enlarge(source_w, source_h, target_w, target_h, operations)
        else:
            # Fallback to copy image.
            # result_image.copy_replace(simg)
            simg.tk.call(result_image.name, "copy", simg.name, "-shrink")

        if operations:
            tmp = simg.copy()
            for cmd in operations:
                action, args = cmd
                if action == "zoom":
                    tmp = tmp.zoom(*args)
                elif action == "subsample":
                    tmp = tmp.subsample(*args)
            # result_image.copy_replace(tmp, shrink=True)
            simg.tk.call(result_image.name, "copy", tmp.name, "-shrink")

        return result_image

    def img_enlarge(
        self, source_w, source_h, target_w, target_h, action_list: list
    ):
        if target_w < source_w or target_h < source_h:
            msg = "target_size should be greater than image size."
            raise RuntimeError(msg)

        # round(number / roundto) * roundto
        xfactor = round((target_w / source_w) / 0.5) * 0.5
        xfactor_par = xfactor % 2 == 0.0
        yfactor = round((target_h / source_h) / 0.5) * 0.5
        yfactor_par = yfactor % 2 == 0.0
        if xfactor_par and yfactor_par:
            # zoom scaling
            cmd = ("zoom", (int(xfactor), int(yfactor)))
            action_list.append(cmd)
        else:
            zoom_xfactor = int(round(target_w * 2 / source_w))
            zoom_yfactor = int(round(target_h * 2 / source_h))
            action_list.append(("zoom", (zoom_xfactor, zoom_yfactor)))
            action_list.append(("subsample", (2,)))

    def img_reduce(
        self, source_w, source_h, target_w, target_h, action_list: list
    ):
        if target_w > source_w or target_h > source_h:
            msg = "target_size should be less than image size."
            raise RuntimeError(msg)

        xfactor = round((source_w / target_w) / 0.5) * 0.5
        xfactor_par = xfactor % 2 == 0.0
        yfactor = round((source_h / target_h) / 0.5) * 0.5
        yfactor_par = yfactor % 2 == 0.0
        if xfactor_par and yfactor_par:
            cmd = ("subsample", (int(xfactor), int(yfactor)))
            action_list.append(cmd)
        else:
            temp_w = target_w * 2
            temp_h = target_h * 2
            if temp_w > source_w and temp_h > source_h:
                self.img_enlarge(
                    source_w, source_h, temp_w, temp_h, action_list
                )
                action_list.append(("subsample", (2,)))
            else:
                ssx = int(round(source_w / (target_w * 2)))
                ssy = int(round(source_h / (target_h * 2)))
                if ssx > 1.0 and ssy > 1.0:
                    cmd = ("subsample", (ssx, ssy))
                    action_list.append(cmd)
                cmd = ("subsample", (2,))
                action_list.append(cmd)
