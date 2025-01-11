# Sphinx extension: Named colors

```{admonition} User types
:class: tip
This section is useful for user type 3-5.
```
+++
{bdg-primary}`Sphinx Extension`

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

::::{note}
In the next part, replace `namedcolor` by the name of the CSS/custom named color.
::::

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

For the named color admonitions the class `show-bar` is introduced for titleless admonitions. This focres printing of the title bar. If a title is given, the title will be printed too and adding the class `show-bar` is redundant. 

::::{warning}
Note that, because of the use of CSS, sometimes results may differ from the expected result.
::::

## Examples & details

### Overview of chosen options for the examples

```yaml
sphinx:
  config:
    named_colors_dark_and_light: true # default value
    named_colors_saturation: 1.5 # default value
    named_colors_include_CSS: true # default value
    named_colors_custom_colors: {'onlylight':[165,21,160],'lightanddark':[45,180,117,204,158,110]}
```

### $\LaTeX$ colors

Some examples of [CSS named colors](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color) and the __custom named colors__ used within LaTeX code. Do not forget to check out the colors in the <span class='only-light'>dark</span><span class='only-dark'>light</span> data-theme!

::::{list-table}
:widths: auto
:header-rows: 1
   * - Color
     - $\LaTeX$ Code
     - Result
   * - olive
     - `\olive{\int_a^bf(x)dx}`
     - $\olive{\int_a^bf(x)dx}$
   * - hotpink
     - `1.\hotpink{\mathbf{48}}`
     - $1.\hotpink{\mathbf{48}}$
   * - darkturquoise
     - `\dfrac{\darkturquoise{\partial}f}{\darkturquoise{\partial}x}`
     - $\dfrac{\darkturquoise{\partial}f}{\darkturquoise{\partial}x}$
   * - onlylight
     - `\onlylight{\LaTeX}`
	 - $\onlylight{\LaTeX}$
   * - lightanddark
     - `\lightanddark{\sum}_{n=1}^\infty`
	 - $\lightanddark{\sum}_{n=1}^\infty$
::::

All of the $\LaTeX$ commands can be used in all components that already support $\LaTeX$.

### MarkDown text colors

The defined roles can be used in regular MarkDown code, similar to other roles such as `numref` and `code`.

::::{list-table}
:widths: auto
:header-rows: 1
   * - Color
     - Style
     - Markdown Code
     - Result
   * - olive
     - regular
     - `` {olive}`regular` ``
     - {olive}`regular`
   * - hotpink
     - strong
     - `` {hotpink_strong}`strong` ``
     - {hotpink_strong}`emphasis`
   * - onlylight
     - emphasis
     - `` {onlylight_emphasis}`emphasis`  ``
     - {onlylight_emphasis}`emphasis`
   * - lightanddark
     - strong emphasis
     - `` {lightanddark_strong_emphasis}`strong emphasis` ``
	 - {lightanddark_strong_emphasis}`strong emphasis`
::::

### Colored admonitions

Any existing admonition supporting the `class` option, whether provided by Sphinx or by a Sphinx extension, can be given a different color by adding a CSS/custom named color to the list of classes.

An alternative option is to use an admonition with the name of the CSS/custom named color and add the type of admonition to the list of classes. In that case and for admonitions without the title argumentbut an automatic title (such as `wanring`), a title has to be set explicitly. This alternative approach does take over numbering (if any) of the oringinal admonition type (if any).

Following are some examples with different colors, with the two code options next to each other, followed by the two results.

A special feature is a new class for existing admonitions: `no-title`. This suppresses printing of the title, even if the title is given. For the named color admonitions this happens automatically if no title is given.

**General admonition**

::::::{grid} 2
:::::{grid-item-card}
```md
::::{admonition} General admonition with title
:class: olive
Content of general admonition.
::::
```
:::::
:::::{grid-item-card}
```md
::::{olive} General admonition with title
Content of general admonition.
::::
```
:::::
::::::

::::::{grid} 2
:::::{grid-item-card}
::::{admonition} General admonition with title
:class: olive
Content of general admonition.
::::
:::::
:::::{grid-item-card}
::::{olive} General admonition with title
Content of general admonition.
::::
:::::
::::::

**Dropwdown admonition**

::::::{grid} 2
:::::{grid-item-card}
```md
::::{admonition} Dropdown admonition with title
:class: hotpink, dropdown
Content of general admonition.
::::
```
:::::
:::::{grid-item-card}
```md
::::{hotpink} Dropdown admonition with title
:class: dropdown
Content of general admonition.
::::
```
:::::
::::::

::::::{grid} 2
:::::{grid-item-card}
::::{admonition} Dropdown admonition with title
:class: hotpink, dropdown
Content of general admonition.
::::
:::::
:::::{grid-item-card}
::::{hotpink} Dropdown admonition with title
:class: dropdown
Content of general admonition.
::::
:::::
::::::

**Common admonitions**

::::::{grid} 2
:::::{grid-item-card}
```md
::::{warning}
:class: darkturquoise
Content of warning.
::::
```
:::::
:::::{grid-item-card}
```md
::::{darkturquoise} Warning
:class: warning
Content of warning.
::::
```
:::::
::::::

::::::{grid} 2
:::::{grid-item-card}
::::{warning}
:class: darkturquoise
Content of warning.
::::
:::::
:::::{grid-item-card}
::::{darkturquoise} Warning
:class: warning
Content of warning.
::::
:::::
::::::

**Admonitions from Sphinx-Proof**

::::::{grid} 2
:::::{grid-item-card}
```md
::::{prf:defintion}
:class: onlylight
Content of definition.
::::
```
:::::
:::::{grid-item-card}
```md
::::{onlylight} Definition
:class: definition
Content of definition.
::::
```
:::::
::::::

::::::{grid} 2
:::::{grid-item-card}
::::{prf:definition}
:class: onlylight
Content of definition.
::::
:::::
:::::{grid-item-card}
::::{onlylight} Definition
:class: definition
Content of definition.
::::
:::::
::::::

**Titleless admonitions**

::::::{grid} 2
:::::{grid-item-card}
```md
::::{admonition} This title will not be shown
:class: lightanddark, no-title
Content of admonition.
::::
```
:::::
:::::{grid-item-card}
```md
::::{lightanddark}
Content of admonition.
::::
```
:::::
::::::

::::::{grid} 2
:::::{grid-item-card}
::::{admonition} This title will not be shown
:class: lightanddark, no-title
Content of admonition.
::::
:::::
:::::{grid-item-card}
::::{lightanddark}
Content of admonition.
::::
:::::
::::::

**Titleless admonitions with dropdown**

In case a dropdown admonition is required without a title, only the new CSS/custum named color admonitions can safely be used.

::::::{grid} 1
:::::{grid-item-card}
```md
::::{lightcoral}
:class: dropdown, warning
Content of admonition.
::::
```
:::::
::::::

::::::{grid} 1
:::::{grid-item-card}
::::{lightcoral}
:class: dropdown, warning
Content of admonition.
::::
:::::
::::::

**Titleless admonitions with title bar**

In case an admonition is required without a title but with a title bar, only the new CSS/custum named color admonitions can safely be used. In that case add the class `show-bar`. 

::::::{grid} 1
:::::{grid-item-card}
```md
::::{gold}
:class: show-bar, warning
Content of admonition.
::::
```
:::::
::::::

::::::{grid} 1
:::::{grid-item-card}
::::{gold}
:class: show-bar, warning
Content of admonition.
::::
:::::
::::::

## Contribute

This tool's repository is stored on [GitHub](https://github.com/TeachBooks/Sphinx-Named-Colors). If you'd like to contribute, you can create a fork and open a pull request on the [GitHub repository](https://github.com/TeachBooks/Sphinx-Named-Colors).

The `README.md` of the branch `manual` is also part of the [TeachBooks manual](https://teachbooks.io/manual/intro.html) as a submodule.