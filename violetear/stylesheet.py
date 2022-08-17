import io
import datetime
from pathlib import Path
from warnings import warn
import textwrap
from .selector import Selector
from .style import Style


class StyleSheet:
    def __init__(self, *styles: Style) -> None:
        self._styles = list(styles)
        self._by_name = {}
        self._used = set()

    def render(self, dynamic: bool = False, fp=None):
        if isinstance(fp, (str, Path)):
            fp = open(fp, "wt")

        if fp is None:
            fp = io.StringIO()

        fp.write("/* Made with violetear */\n")
        if dynamic:
            fp.write(f"/* Generating {len(self._used)}/{len(self._by_name)} styles */\n")
        else:
            fp.write(f"/* Generating all {len(self._by_name)} styles */\n")
        fp.write(f"/* Autogenerated on {datetime.datetime.now()} */\n\n")

        for style in self._styles:
            fp.write(style.css())
            fp.write("\n\n")

        if isinstance(fp, io.StringIO):
            result = fp.getvalue()
        else:
            result = None

        fp.close()
        return result

    def add(self, selector: str, style:Style=None, *, name:str=None) -> Style:
        if not name:
            name = selector.replace("#", "_").replace(".", "_").replace("-","_").strip("_")

        if not style:
            style = Style(Selector.from_css(selector))

        self._styles.append(style)
        self._by_name[name] = style
        return style

    def media(self, min_width: int = None, max_width: int = None) -> "MediaSet":
        media = MediaSet(self, min_width=min_width, max_width=max_width)
        self._styles.append(media)
        return media

    def redefine(self, style: Style) -> Style:
        style = Style(selector=style._selector)
        self._styles.append(style)
        return style

    def __getitem__(self, key) -> Style:
        try:
            style = self._by_name[key]
            self._used.add(style)
            return style
        except KeyError:
            warn(f"Style {key} not defined")
            raise

    def __getattr__(self, key) -> Style:
        return self[key]

class MediaSet(StyleSheet):
    def __init__(
        self, sheet: StyleSheet, min_width: int = None, max_width: int = None
    ) -> None:
        super().__init__()

        self._min_width = min_width
        self._max_width = max_width
        self._sheet = sheet

    def render(self, dynamic: bool = False, fp=None, used=None):
        query = []

        if self._min_width:
            query.append(f"min-width: {self._min_width}px")

        if self._max_width:
            query.append(f"max-width: {self._max_width}px")

        fp.write(f"\n@media({', '.join(query)})")
        fp.write("{\n")

        for style in self._styles:
            style.render(dynamic=dynamic, fp=fp, used=used)
            fp.write("\n")

        fp.write("}\n")
