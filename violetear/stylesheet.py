# # Style Sheets

"""This module defines the `StyleSheet` class, which encapsulates a collection of CSS styles
and allows rendering stylesheets either as files or as strings to be injected inline.
"""

# Regular imports:

import io
import datetime
from pathlib import Path
from typing import Set
from warnings import warn
import textwrap

from violetear.animation import Animation

# Internal imports:

from .selector import Selector
from .style import Style
from .media import MediaQuery

# ## The `StyleSheet` class


class StyleSheet:
    def __init__(
        self, *styles: Style, normalize: bool = True, base: Style = None
    ) -> None:
        """Initializes a new StyleSheet, optionally with a set of initial styles
        and a base style for inheritance.

        **Parameters**:

        - `styles`: A sequence of initial styles to add.
        - `normalize`: If `True` then the stylesheet will contain a set of normalization
                       rules taken from <https://github.com/sindresorhus/modern-normalize>.
        - `base`: A style to use as base for all newly defined styles
                  (i.e., any new style will `apply` the base style).
        """
        self.styles = []
        self.medias = []
        self._by_name = {}
        self._by_selector = {}
        self._used = set()
        self._media = None
        self._base = base

        for style in styles:
            self.add(style)

        if normalize:
            self._preamble = open(Path(__file__).parent / "normalize.css").read()
        else:
            self._preamble = None

    # ### Rendering methods

    # #### `StyleSheet.render`

    # This method renders the stylesheet to CSS. It can work in two ways:
    # either to write the rules to a file, or to return the rules as a string.
    # Both ways are implemented using a file, either passed as parameter, or
    # using an `io.StringIO` instance to generate an in-memory string.

    # Additionally this method can render a "dynamic" file, which means
    # just outputting the rules that are being used.

    def render(self, fp=None, *, dynamic: bool = False):
        """Render the stylesheet either to a file or a string.

        **Parameters**:

        - `fp`: A file-like object, or a path, to render to a file.
                If `fp=None`, then a string is returned.
        - `dynamic`: If `True` then only the styles used (i.e., accessed through
                     the attribute or dict interfaces) are rendered.
                     This is useful when you inject the stylesheet into a template.
        """

        # First we will decide whether to render to a file or a string.
        # We will keep track of when we call `open` to make sure to call `close`.
        # If `fp` is a path-like, we'll open it, and if it's `None`, we'll create
        # an `io.StringIO` file to render to memory and return the stylesheet as a string.

        opened = False

        if isinstance(fp, (str, Path)):
            fp = open(fp, "wt")
            opened = True

        if fp is None:
            fp = io.StringIO()
            opened = True

        # Now we can write all the rules into `fp` regardless of what it is.
        # First the preamble (which can be empty or the content of normalize.css),
        # and then all the defined styles (including sub-styles).
        # Finally, all media-conditioned styles are rendered, wrapped appropiately.

        self._write_preamble(fp)
        total = 0
        animations: Set[Animation] = set()  # To collect all defined animations

        for style in self.styles:
            total += self._render(style, fp, 0, animations)

        for media in self.medias:
            fp.write(media.css())
            fp.write("{\n")

            for style in media.styles:
                total += self._render(style, fp, 4, animations)

            fp.write("}\n\n")

        # Generate all animations, but each one only once.

        for animation in sorted(animations, key=lambda a: a.name):
            fp.write(animation.css())
            fp.write("\n\n")

        # And now we can close the file if we opened it,
        # and decide whether to return a string or not depending on the
        # type of file we have.

        fp.write(f"/* Generated {total} styles */")

        if isinstance(fp, io.StringIO):
            result = fp.getvalue()
        else:
            result = None

        if opened:
            fp.close()

        return result

    # ### Rendering helpers

    def _write_preamble(self, fp):
        fp.write("/* Made with violetear */\n")
        fp.write("/* This file is autogenerated. Do not modify. */\n\n")

        fp.write(self._preamble)

        if self._preamble:
            fp.write("\n")

    def _render(self, style: Style, fp, indent, animations):
        total = 0

        for s in [style] + list(style._children.values()):
            if not s._rules:
                continue

            fp.write(textwrap.indent(s.css(), indent * " "))
            fp.write("\n\n")
            total += 1

            for animation in s._animations:
                animations.add(animation)

        return total

    # ### Manipulating styles

    def select(self, selector: str, *, name: str = None) -> Style:

        if name is None:
            name = (
                selector.replace("#", "_")
                .replace(".", "_")
                .replace("-", "_")
                .strip("_")
            )

        style = self._by_selector.get(selector)

        if style is not None:
            self._by_name[name] = style
            return style

        style = Style(Selector.from_css(selector))

        if self._base:
            style.apply(self._base)

        return self.add(style, name=name)

    def add(self, style: Style = None, *, name: str = None) -> Style:
        if self._media is None:
            self.styles.append(style)
        else:
            self._media.add(style)

        if name is not None:
            self._by_name[name] = style

        return style

    def extend(self, other: "StyleSheet") -> "StyleSheet":
        for style in other.styles:
            self.add(style)

        for name, style in other._by_name.items():
            self._by_name[name] = style

        for selector, style in other._by_selector.items():
            self._by_selector[selector] = style

        for media in other.medias:
            self.medias.append(media.clone(self))

        return self

    def media(self, min_width: int = None, max_width: int = None) -> MediaQuery:
        media = MediaQuery(self, min_width=min_width, max_width=max_width)
        self.medias.append(media)
        return media

    def redefine(self, style: Style) -> Style:
        style = Style(selector=style.selector)
        self.add(style=style)
        return style

    # ### Accessors

    # These methods allow accesing styles with the `sheet["style"]` and `sheet.style` syntax.
    # This is mostly relevant when using a template engine to inject the stylesheet into
    # the template and render the styles inline.

    def __getitem__(self, key) -> Style:
        try:
            style = self._by_name[key]
            self._used.add(style)
            return style
        except KeyError:  # This is necessary because template engines will
            warn(
                f"Style {key} not defined"
            )  # often silence `KeyError` exceptions and instead
            raise  # return `None`, so you at least see a warning.

    def __getattr__(self, key) -> Style:
        return self[key]
