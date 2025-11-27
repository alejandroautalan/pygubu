from dataclasses import dataclass, field, asdict, replace
from typing import List, Dict, Optional, Iterator
from enum import Enum, auto


class ThemeType(Enum):
    LIGHT = auto()
    DARK = auto()


@dataclass
class IconItem:
    fn: str
    width: Optional[int] = None
    color_override: Optional[bool] = None
    color_onlight: Optional[str] = None
    color_ondark: Optional[str] = None
    custom: Optional[bool] = None

    def asdict_cleaned(self) -> dict:
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
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
    icons: Dict[str, IconItem] = field(default_factory=dict)
    custom_files: Dict[str, str] = field(default_factory=dict)

    def iter_items(self, theme=ThemeType.LIGHT) -> Iterator:
        for item in self.icons.values():
            yield self._item_for_theme(item, theme)

    def item(self, uid, theme=ThemeType.LIGHT) -> IconItem:
        found_item = self.icons[uid]
        return self._item_for_theme(found_item, theme)

    def _item_for_theme(self, item: IconItem, theme: ThemeType) -> IconItem:
        item_values = dict(
            color_override=True,
            color_ondark=self.color_ondark,
            color_onlight=self.color_onlight,
            width=self.icon_width,
            custom=False,
        )
        item_values.update(item.asdict_cleaned())
        return IconItem(**item_values)

    @staticmethod
    def from_dict(iconset_definition: dict):
        icons = {
            key: IconItem(**values)
            for key, values in iconset_definition["icons"].items()
        }
        iconset_definition["icons"] = icons
        return IconSet(**iconset_definition)

    @staticmethod
    def to_dict(iconset: "IconSet") -> dict:
        definition = asdict(iconset)
        icons = definition["icons"]
        for key, values in icons.items():
            cleaned = {
                key: value for key, value in values.items() if value is not None
            }
            icons[key] = cleaned
        return definition
