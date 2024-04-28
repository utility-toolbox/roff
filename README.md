# roff
python-based cli to convert markdown to the roff (man-pages) format

![roff-manpage head](https://github.com/utility-toolbox/roff/blob/main/README.assets/roff-manpage-head.png?raw=true)

<!-- TOC -->
* [roff](#roff)
  * [Installation](#installation)
  * [Usage/Execution](#usageexecution)
  * [File Format](#file-format)
  * [Example](#example)
<!-- TOC -->

## Installation

[![PyPI - Version](https://img.shields.io/pypi/v/roff)
](https://pypi.org/project/roff/)

```shell
pip install roff
pip install roff[images]  # support for images
pip install roff[images-svg]  # support for svg-images
```

> [!TIP] 
> After the installation you should be able to see [roff's manpage](https://github.com/utility-toolbox/roff/blob/main/docs/roff.1.md) with `man roff`
> or the file format information with `man roff.5`.

## Usage/Execution

```shell
roff --help
roff template command.1.md
roff convert command.1.md
man ./command.1
```

## File Format

`roff` uses markdown as the file format. It supports all commonmark markdown features (h1 is reserved for the head).

Additionally, roff brings 1 own markdown-feature, the `inline-command`!
By prepending your inline-code with a `$` sign it gets recognised as an inline-command and rendered in a more special way.

```markdown
$`command subcommand [--arg value] file...`
```

![example: inline-command](README.assets/example-inline-command.png)

> [!TIP]
> Use `roff template command.1.md` to get a pre-filled markdown file as a starting point.

## Example

The following image shows the manpage of roff itself 

![example: manpage](https://github.com/utility-toolbox/roff/blob/main/README.assets/roff-manpage.png?raw=true)
