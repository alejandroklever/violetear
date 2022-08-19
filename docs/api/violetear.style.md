??? note "Docstring"
    This module defines the `Style` class.


## Top level imports

These are for typing our methods:



```python linenums="5"
from typing import List, Tuple, Union
```

These ones are internal to `violetear`:



```python linenums="7"
from .selector import Selector
from .units import GridSize, GridTemplate, Unit, fr, pc, minmax, repeat
from .color import Color
from .helpers import style_method
```

And this one is for generating CSS:



```python linenums="12"
import textwrap
```

## The `Style` class

The `Style` class is the main concept in `violetear`.
It encapsulates the functionality to generate CSS rules.
In summary, a `Style` is defined by a CSS selector
(represented in the [`Selector`](../violetear.selector/#ref:Selector) class)
and a set of rules, internally implemented with dictionary that maps attributes to values.

The `Style` class provides a main [`rule`](../violetear.style/#ref:Style.rule) method to manually set any CSS rule.
However, to simplify usage, the most common CSS rules are encapsulated in fluent methods
that allow chained invocation to quickly build a complex style.

<a name="ref:Style"></a>

```python linenums="22"
class Style:
    def __init__(
        self, selector: Union[str, Selector] = None, *, parent: "Style" = None
    ) -> None:
```

??? note "Docstring"
    Create a new instance of `Style`.
    
    **Parameters**:
    
    - `selector`: The selector to which this style applies. Can be `None`, or a string,
    in which case it is parsed with `Selector.from_css`.
    - `parent`: An optional parent style (e.g., if this is an state or children style) so
    that when checking which styles are used, the parent can be referenced.




```python linenums="35"
        if isinstance(selector, str):
            selector = Selector.from_css(selector)

        self.selector = selector
        self._rules = {}
        self._parent = parent
        self._children = []
```

### Basic rule manipulation

These methods allows manipulating rules manually.

#### `Style.rule`
The `rule` method simply adds a rule to the internal dictionary.



```python linenums="46"
    def rule(self, attr: str, value) -> "Style":
```

??? note "Docstring"
    Define a new CSS rule.
    
    **Parameters**:
    
    - `attr`: a CSS attribute (e.g., `'font-size'`)
    - `value`: a value for the attribute. It will be converted to `str` internally.




```python linenums="54"
        self._rules[attr] = str(value)
        return self
```

#### `Style.apply`
The `apply` method enables style composition, by copying all the rules
in one or more input styles into this style.



```python linenums="59"
    def apply(self, *others: "Style") -> "Style":
        for other in others:
            for attr, value in other._rules.items():
                self.rule(attr, value)

        return self
```

### Typography styles



```python linenums="66"
    @style_method
    def font(
        self, size: Unit = None, *, weight: str = None, family: str = None
    ) -> "Style":
        if size:
            self.rule("font-size", Unit.infer(size))

        if weight:
            self.rule("font-weight", weight)

        if family:
            self.rule("font-family", family)

    @style_method
    def text(self, *, align: str = None) -> "Style":
        if align is not None:
            self.rule("text-align", align)

    @style_method
    def center(self) -> "Style":
        self.text(align="center")

    @style_method
    def left(self) -> "Style":
        self.text(align="left")

    @style_method
    def right(self) -> "Style":
        self.text(align="right")

    @style_method
    def justify(self) -> "Style":
        self.text(align="justify")
```

### Color styles



```python linenums="100"
    @style_method
    def color(
        self, color: Color = None, *, rgb=None, hsv=None, hls=None, alpha: float = None
    ) -> "Style":
        if color is None:
            if rgb is not None:
                r, g, b = rgb
                color = Color(r, g, b, alpha)
            elif hsv is not None:
                h, s, v = hsv
                color = Color.from_hsv(h, s, v, alpha)
            elif hls is not None:
                h, l, s = hls
                color = Color.from_hls(h, l, s, alpha)

        self.rule("color", color)

    @style_method
    def background(
        self, color: Color = None, *, rgb=None, hsv=None, hls=None, alpha: float = None
    ) -> "Style":
        if color is None:
            if rgb is not None:
                r, g, b = rgb
                color = Color(r, g, b, alpha)
            elif hsv is not None:
                h, s, v = hsv
                color = Color.from_hsv(h, s, v, alpha)
            elif hls is not None:
                h, l, s = hls
                color = Color.from_hls(h, l, s, alpha)

        self.rule("background-color", color)
```

### Visibility styles



```python linenums="134"
    @style_method
    def visibility(self, visibility: str) -> "Style":
        self.rule("visibility", visibility)

    @style_method
    def visible(self) -> "Style":
        self.visibility("visible")

    @style_method
    def hidden(self) -> "Style":
        self.visibility("hidden")
```

### Geometry styles



```python linenums="146"
    @style_method
    def width(self, value=None, *, min=None, max=None) -> "Style":
        if value is not None:
            self.rule("width", Unit.infer(value, on_float=pc))

        if min is not None:
            self.rule("min-width", Unit.infer(min, on_float=pc))

        if max is not None:
            self.rule("max-width", Unit.infer(max, on_float=pc))

    @style_method
    def height(self, value=None, *, min=None, max=None) -> "Style":
        if value is not None:
            self.rule("height", Unit.infer(value, on_float=pc))

        if min is not None:
            self.rule("min-height", Unit.infer(min, on_float=pc))

        if max is not None:
            self.rule("max-height", Unit.infer(max, on_float=pc))

    @style_method
    def margin(self, all=None, *, left=None, right=None, top=None, bottom=None) -> "Style":
        if all is not None:
            self.rule("margin", Unit.infer(all))
        if left is not None:
            self.rule("margin-left", Unit.infer(left))
        if right is not None:
            self.rule("margin-right", Unit.infer(right))
        if top is not None:
            self.rule("margin-top", Unit.infer(top))
        if bottom is not None:
            self.rule("margin-bottom", Unit.infer(bottom))

    @style_method
    def padding(self, all=None, *, left=None, right=None, top=None, bottom=None) -> "Style":
        if all is not None:
            self.rule("padding", Unit.infer(all))
        if left is not None:
            self.rule("padding-left", Unit.infer(left))
        if right is not None:
            self.rule("padding-right", Unit.infer(right))
        if top is not None:
            self.rule("padding-top", Unit.infer(top))
        if bottom is not None:
            self.rule("padding-bottom", Unit.infer(bottom))

    @style_method
    def rounded(self, radius: Unit = None) -> "Style":
        if radius is None:
            radius = 0.25

        self.rule("border-radius", Unit.infer(radius))
```

### Layout styles



```python linenums="201"
    @style_method
    def display(self, display: str) -> "Style":
        self.rule("display", display)

    @style_method
    def flexbox(
        self,
        direction: str = "row",
        *,
        wrap: bool = False,
        reverse: bool = False,
        align: str = None,
        justify: str = None,
    ) -> "Style":
        self.display("flex")

        if reverse:
            direction += "-reverse"

        self.rule("flex-direction", direction)

        if wrap:
            self.rule("flex-wrap", "wrap")

        if align is not None:
            self.rule("align-items", align)

        if justify is not None:
            self.rule("justify-content", justify)

    @style_method
    def flex(
        self, grow: float = None, shrink: float = None, basis: int = None,
    ) -> "Style":
        if grow is not None:
            self.rule("flex-grow", float(grow))

        if shrink is not None:
            self.rule("flex-shrink", float(shrink))

        if basis is not None:
            self.rule("flex-basis", Unit.infer(basis, on_float=fr))

    @style_method
    def grid(
        self,
        *,
        columns: Union[int, List[GridTemplate]] = None,
        rows: Union[int, List[GridTemplate]] = None,
        auto_columns: GridSize = None,
        auto_rows: GridSize = None,
        gap: Unit = 0,
    ) -> "Style":
        self.display("grid")

        if columns is None and rows is None:
            raise ValueError("Either columns or rows must be specified")

        if isinstance(columns, int):
            columns = repeat(columns, fr(1))

        if isinstance(rows, int):
            rows = repeat(rows, fr(1))

        if columns is not None:
            self.rule("grid-template-columns", columns)
        elif auto_columns is not None:
            self.rule("grid-auto-columns", auto_columns)

        if rows is not None:
            self.rule("grid-template-rows", rows)
        elif auto_rows is not None:
            self.rule("grid-auto-rows", auto_rows)

        self.rule("gap", Unit.infer(gap, on_float=fr))

    @style_method
    def columns(
        self, count: int, min: GridSize = None, max: GridSize = None, *, gap: Unit = 0
    ) -> "Style":
        if min is None:
            min = fr(1)

        if max is None:
            max = fr(1)

        self.grid(columns=repeat(count, minmax(min, max)), gap=gap)

    @style_method
    def rows(
        self, count: int, min: GridSize = None, max: GridSize = None, *, gap: Unit = 0
    ) -> "Style":
        if min is None:
            min = fr(1)

        if max is None:
            max = fr(1)

        self.grid(rows=repeat(count, minmax(min, max)), gap=gap)

    @style_method
    def place(
        self,
        columns: Union[int, Tuple[int, int]] = None,
        rows: Union[int, Tuple[int, int]] = None,
    ) -> "Style":
        if columns is not None:
            if isinstance(columns, tuple):
                columns = f"{columns[0]} / {columns[1]+1}"

            self.rule("grid-column", columns)

        if rows is not None:
            if isinstance(rows, tuple):
                rows = f"{rows[0]} / {rows[1]+1}"

            self.rule("grid-row", rows)

    @style_method
    def position(
        self,
        position: str,
        *,
        left: int = None,
        right: int = None,
        top: int = None,
        bottom: int = None,
    ) -> "Style":
        self.rule("position", position)

        if left is not None:
            self.rule("left", Unit.infer(left))
        if right is not None:
            self.rule("right", Unit.infer(right))
        if top is not None:
            self.rule("top", Unit.infer(top))
        if bottom is not None:
            self.rule("bottom", Unit.infer(bottom))

    @style_method
    def absolute(
        self,
        *,
        left: int = None,
        right: int = None,
        top: int = None,
        bottom: int = None,
    ) -> "Style":
        self.position("absolute", left=left, right=right, top=top, bottom=bottom)

    @style_method
    def relative(
        self,
        *,
        left: int = None,
        right: int = None,
        top: int = None,
        bottom: int = None,
    ) -> "Style":
        self.position("relative", left=left, right=right, top=top, bottom=bottom)
```

### Sub-styles



```python linenums="362"
    def on(self, state) -> "Style":
        style = Style(self.selector.on(state))
        self._children.append(style)
        return style

    def children(self, selector: str = "*", *, nth: int = None) -> "Style":
        style = Style(self.selector.children(selector, nth=nth))
        self._children.append(style)
        return style
```

### Rendering methods



```python linenums="372"
    def css(self, inline: bool = False) -> str:
        separator = "" if inline else "\n"

        rules = separator.join(
            f"{attr}: {value};" for attr, value in self._rules.items()
        )

        if inline:
            return rules

        return f"{self.selector.css()} {{\n{textwrap.indent(rules, 4*' ')}\n}}"

    def inline(self) -> str:
        return f'style="{self.css(inline=True)}"'

    def markup(self) -> str:
        return self.selector.markup()

    def __str__(self):
        return self.markup()
```
