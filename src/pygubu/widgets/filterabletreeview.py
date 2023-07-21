import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable, Optional


_filter_func = Callable[[ttk.Treeview, str, str], bool]


class BasicFilter:
    def __call__(self, tree, itemid, filter_value: str) -> bool:
        # Default filter match function.
        txt = tree.item(itemid, "text").lower()
        match_found = filter_value in txt
        return match_found


class FilterableTreeview(ttk.Treeview):
    def __init__(self, *args, filter_func: Optional[_filter_func] = None, **kw):
        super().__init__(*args, **kw)
        self.filter_active = False
        self.filter_value = ""
        self.filter_prev_value = None
        self.filter_prev_selitem = None
        self._detached = []
        self._expanded = set()
        self.filter_func = BasicFilter() if filter_func is None else filter_func

    #
    # Filter functions
    #
    def _see(self, item):
        # The item may have been deleted.
        if self.exists(item):
            self.see(item)

    def _see_later(self, item):
        self.after_idle(lambda: self._see(item))

    def filter_by(self, fvalue):
        """Filters treeview"""

        self.filter_remove()
        if not fvalue:
            return

        self.filter_value = fvalue
        # self._expand_all()
        self.selection_set("")

        children = self.get_children("")
        for item in children:
            match_, detached = self._filter_and_detach(item)
            if detached:
                self._detached.extend(detached)
            if match_:
                self.item(item, open=True)
        for i, p, idx in self._detached:
            self.detach(i)
        self.filter_active = True

    def filter_remove(self, remember=False):
        """Removes filter and reattaches hidden items.
        When filter is applied you can not traverse through detached items.
        So to be able to navigate all tree items with filter active you use
        the following approach:

          tree.filter_remove(remember=True)
          # Do operation, navigate tree items.
          tree.filter_restore()
        """
        if self.filter_active:
            sitem = None
            selection = self.selection()
            if selection:
                sitem = selection[0]
                self._see_later(sitem)
            if remember:
                self.filter_prev_value = self.filter_value
                self.filter_prev_selitem = sitem
            self._reattach()
            self._restore_open_state()
            self.filter_value = ""
        self.filter_active = False

    def filter_restore(self):
        if self.filter_prev_value:
            self.filter_value = self.filter_prev_value
            item = self.filter_prev_selitem
            if item and self.exists(item):
                self.selection_set(item)
                self._see_later(item)
            # clear
            self.filter_prev_value = ""
            self.filter_prev_selitem = None
            # Re apply filter?
            self.filter_by(self.filter_value)

    def expand_to(self, target_item, start_item=""):
        """Search and expand tree to see itemid."""
        self._expand_to(start_item, target_item)

    def _expand_to(self, rootitem, target_item):
        found = rootitem == target_item
        if not found:
            children = self.get_children(rootitem)
            found = target_item in children
            if not found:
                for child_item in children:
                    found = self._expand_to(child_item, target_item)
                    if found:
                        break
        if found and rootitem != "":
            self.item(rootitem, open=True)
        return found

    def expand_all(self, rootitem=""):
        children = self.get_children(rootitem)
        for item in children:
            self._expand_all(item)
        if rootitem != "" and children:
            self.item(rootitem, open=True)

    def _restore_open_state(self, rootitem=""):
        if rootitem != "":
            was_open = rootitem in self._expanded
            self.item(rootitem, open=was_open)
        children = self.get_children(rootitem)
        for item in children:
            self._restore_open_state(item)
        if rootitem == "":
            # End of recursion clear expanded set
            self._expanded.clear()

    def _reattach(self):
        """Reinsert the hidden items."""
        for item, p, idx in self._detached:
            # The item may have been deleted.
            if self.exists(item) and self.exists(p):
                self.move(item, p, idx)
        self._detached = []

    def _filter_and_detach(self, item) -> (bool, list):
        """Hide items from treeview that do not match the search string."""
        to_detach = []
        children_det = []
        children_match = False
        if self.item(item, "open"):
            self._expanded.add(item)
        match_found = self.filter_func(self, item, self.filter_value)
        parent = self.parent(item)
        idx = self.index(item)
        children = self.get_children(item)
        if children:
            for child in children:
                match, detach = self._filter_and_detach(child)
                children_match = children_match | match
                if detach:
                    children_det.extend(detach)
        if match_found:
            self.item(item, open=True)
            if children_det:
                to_detach.extend(children_det)
        else:
            if children_match:
                self.item(item, open=True)
                if children_det:
                    to_detach.extend(children_det)
            else:
                to_detach.append((item, parent, idx))
        match_found = match_found | children_match
        return match_found, to_detach

    #
    # End Filter functions
    #
