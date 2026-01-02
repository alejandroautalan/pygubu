from dataclasses import dataclass, field, asdict, replace
from typing import List, Dict, Optional, Iterator
from enum import Enum, auto


class ThemeType(Enum):
    LIGHT = auto()
    DARK = auto()


@dataclass
class IconItem:
    fn: str
    uid: Optional[str] = None
    width: Optional[int] = None
    color_keep: Optional[bool] = None
    color_onlight: Optional[str] = None
    color_ondark: Optional[str] = None
    custom: Optional[bool] = None

    def asdict_cleaned(self, empty_values=None) -> dict:
        if empty_values is None:
            empty_values = {}
        return {
            key: value
            for key, value in asdict(self).items()
            if (value is not None and value != empty_values.get(key, None))
        }


@dataclass
class IconSet:
    version: int
    name: str
    docs: str
    icon_width: int
    color_onlight: str = "#ffffff"
    color_ondark: str = "#000000"
    with_png: bool = False
    with_gif: bool = False
    icons: List[IconItem] = field(default_factory=list)
    custom_files: Dict[str, str] = field(default_factory=dict)

    def __contains__(self, item: str):
        return self.item_by_uid(item) is not None

    def item_by_uid(self, uid) -> IconItem:
        found = None
        for item in self.icons:
            if item.uid == uid:
                found = item
        return found

    def iter_items_on_theme(self, theme=ThemeType.LIGHT) -> Iterator:
        for item in self.icons:
            yield self._item_for_theme(item, theme)

    def item_on_theme(self, uid, theme=ThemeType.LIGHT) -> IconItem:
        found_item = self.item_by_uid(uid)
        return self._item_for_theme(found_item, theme)

    def _item_for_theme(self, item: IconItem, theme: ThemeType) -> IconItem:
        item_values = dict(
            color_keep=False,
            color_ondark=self.color_ondark,
            color_onlight=self.color_onlight,
            width=self.icon_width,
            custom=False,
        )
        item_values.update(item.asdict_cleaned())
        return IconItem(**item_values)

    @classmethod
    def from_dict(cls, iconset_definition: dict):
        icons = [
            IconItem(**item_values)
            for item_values in iconset_definition["icons"]
        ]
        iconset_definition["icons"] = icons
        return cls(**iconset_definition)

    @staticmethod
    def to_dict(iconset: "IconSet", empty_values=None) -> dict:
        definition = asdict(iconset)
        cleaned = []
        for item in iconset.icons:
            cleaned.append(item.asdict_cleaned(empty_values))
        definition["icons"] = cleaned
        return definition
