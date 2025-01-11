# Sphinx extension: Named colors

## Introduction

This extensions provides a simple solution to use [CSS named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color) and ___custom named colors___ in:
- $\LaTeX$;
- MarkDown text;
- Admonitions.

## What does it do?

This extension defines, based on the CSS named color and custom named colors (provided by the user), several new
- $\LaTeX$ commands;
- Sphinx roles;
- Sphinx admonitions;
- Sphinx admonition classes;

that are styled by a generated CSS file.

If specified, each color will have a different value in the light and dark data-theme. 

## Installation
To use this extenstion, follow these steps:

**Step 1: Install the Package**

Install the `sphinx-named-colors` package using `pip`:
```
pip install sphinx-named-colors
```

**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
sphinx-named-colors
```

**Step 3: Enable in `_config.yml`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions (**important**: underscore, not dash this time):
```
sphinx: 
    extra_extensions:
        .
        .
        .
        - sphinx_named_colors
        .
        .
        .
```

## Configuration

This extension provides the following configuration values:

```yaml
named_colors_include_CSS: true # default value
```

- If set to _true_ all [CSS named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color) will be included in the extension.
- If set to _false_ no [CSS named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color) will be included in the extension. If no custom named colors are defined, this extension will do nothing.

```yaml
named_colors_dark_and_light: true # default value
```

- _true_: for all [CSS named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color) and all custom named colors a secondary value will be generated for use in the dark data-theme, unless otherwise specifed for custom colors. The generated colors emulate the same as the CSS filter `invert(1) hue_rotate(180) saturate(<val>);` where `<val>` is the value set by `named_colors_saturation`.
- _false_: This disables the use of different colors in the dark data-theme, even if specified for custom colors.

```yaml
named_colors_saturation: 1.5 # default value
```

- _number_: The saturation value used in the generation of the dark data-theme colors.

```yaml
named_colors_custom_colors: None
```

- _None_: No custom named colors will be included.
- _dictionary_: A Python dictionary where each `key` defines a custom name and the `value` is a list of 3 or 6 integers, with each integer at minimum 0 and at maximum 255.
  - If 3 integers are provided, these are the RGB values of the custom named color and, if specified, the dark data-theme color will be generated.
  - If 6 integers are provided, the first set of 3 integers form the RGB values of the custom named color and the second set of 3 integers form the RGB values of the dark data-theme color.
  - Each key should contain only characters from the ranges `a-z`.
  - An example value:
    - `` {'onlylight':[165,21,160],'lightanddark':[45,180,117,204,158,110]} ``

## Provided code

> [!NOTE]
> In the next part, replace `namedcolor` by the name of the CSS/custom named color.

### $\LaTeX$ elements

```latex
\namedcolor{...}
```

- Only use in $\LaTeX$ code.
- This will typeset `...` in the color _namedcolor_.

### MarkDown elements

```md
{namedcolor}`...`
```

- Only use in _MarkDown_ code.
- This will typeset `...` in the color _namedcolor_.

To provide the use of {strong}`strong` and/or {emphasis}`emphasis` colored text, we als provide the next three roles:

```md
{namedcolor_strong}`...`
```

```md
{namedcolor_emphasis}`...`
```

```md
{namedcolor_strong_emphasis}`...`
```

These extra roles have been created using the extension [sphinxnotes-comboroles](https://sphinx.silverrainz.me/comboroles/).

### Admonitions

Colored admonitions can be generated in two ways, explained below.

**1. By adding a class to an existing admonition**

```md
::::{type} Title (optional or required, depending on type)
:class: namedcolor
Content
::::
```

**2. By using a new admonition**

```md
::::{namedcolor} Title (optional)
Content
::::
```

If the title is omitted in the new admonition, the title bar will not be displayed.

In both cases extra classes can be added to the admonition to apply other styling.

A special new class for existing admonitions is also introduced: `no-title`. This suppresses printing of the title bar, even if the title is given. For the named color admonitions this happens automatically if no title is given.

For the named color admonitions the class `show-bar` is introduced for titleless admonitions. This forces printing of the title bar. If a title is given, the title will be printed too and adding the class `show-bar` is redundant.

> [!WARNING]
> Note that, because of the use of CSS, sometimes results may differ from the expected result.

## Examples & details

To see examples of usage visit [this page in the TeachBooks manual](https://teachbooks.io/manual/intro.html).

## Contribute

This tool's repository is stored on [GitHub](https://github.com/TeachBooks/Sphinx-Named-Colors). If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/Sphinx-Named-Colors).

The `README.md` of the branch `manual` is also part of the [TeachBooks manual](https://teachbooks.io/manual/intro.html) as a submodule.
