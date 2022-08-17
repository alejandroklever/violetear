# violetear

![PyPI](https://img.shields.io/pypi/v/violetear)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/violetear)
![PyPI - License](https://img.shields.io/pypi/l/violetear)

> A minimalist CSS generator

`violetear` is a minimalist CSS generator in Python. You write Python code and obtain a CSS definition, that you can either render to a file and serve statically, inject dynamically into your HTML, or use as inline styles directly in your markup.

## Why?

For fun, mostly... but also, because CSS is boring and repetitive. As a style language, CSS is great at describing the most varied designs. However, in terms of productivity, CSS lacks three core features that make programming languages useful: abstraction, encapsulation, and reusability.

Using a general-purpose programming language to generate CSS we can obtain the best of both worlds: the expresivity of a declarative with the productivity of an imperative language.

## What?

`violetear` is a bridge between Python and CSS. The simplest use case is a fluid API for generating CSS, full with code completion, documentation, and shorthand methods for the most common CSS rule sets.

But it gets better quickly. Using `violetear` you can compose simpler styles into more complex ones, reusing common rules to reduce repetition to a minimum. This way you can build up complex layouts via composition.

You can manipulate magnitudes, such as colors, making it much easier to generate a specific color pallete, for instance. Since you have a full-featured programming language, you can leverage variables and methods to, for example, generate dynamic themes on-the-fly based on user-defined preferences.

Finally, `violetear` can generate only the subset of styles used in any given template from a single Pyhon source. This means you can happily define all your styles globally and then deliver the minimum CSS subset necessary for each view.

## How?

`violetear` is a pure Python package with zero dependencies. Install it with:

```bash
pip install violetear
```

Next, create a stylesheet:

```python
from violetear import StyleSheet

sheet = StyleSheet()
```

Then you add your styles using common CSS selectors and a fluid API to quickly build complex rule sets:

```python
title = sheet.add("#title").font(14, weight="lighter").margin(5, top=0)
subtitle = sheet.add(".subtitle").apply(title).font(12)
```

You can add conditional (media query) styles with a simple API:

```python
with sheet.media(min_width=768):
    sheet.redefine(title).display("inline")
```

Once your stylesheet is complete, you have a few options to deliver the styles to your frontend.

You can render the stylesheet into a static file:

```python
sheet.render("static/css/main.css")
```

Or you can embed it into your HTML (e.g, using Jinja):

```html
...
<style>
    {{ style.render() }}
</style>
...
```