# roff
python-based cli to convert markdown to the roff (man-pages) format

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

> Tip: after the installation you should be able to see [roff's manpage](https://github.com/utility-toolbox/roff/blob/main/docs/roff.1.md) with `man roff` 

## Usage/Execution

```shell
roff --help
roff template command.1.md
roff convert command.1.md
man ./command.1
```

## File Format

`roff` uses markdown as the file format. It supports all commonmark markdown features (headers are limited to h2-h4).

Additionally, roff brings 1 own markdown-feature, the `inline-command`!
By prepending your inline-code with a `$` sign it gets recognised as an inline-command and rendered in a more special way.

```markdown
$`command subcommand [--arg value] file...`
```

![example: inline-command](README.assets/example-inline-command.png)

> [!TIP]
> Use `roff template command.1.md` to get a pre-filled markdown file as a starting point.

## Example

> [!WARNING]
> This example is from a previous version and slightly outdated.

<details>
  <summary>Corresponding Markdown</summary>

````markdown
roff(1) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## SYNOPSIS

- `roff [-h] [-v] {convert,template} ...`
- `roff convert [-h] source [dest]`
- `roff template [-h] dest`

## DESCRIPTION

python-based cli to convert markdown to the roff (man-pages) format.  
nextline

  indented

> blockquote

```python
import roff

with roff.Converter():
    print("Hey")
```

## OPTIONS

### `convert`

* `source`:
Markdown file that should be parsed

* `[dest]`:
Manpage file

### `template`

* `dest`:
Target file that should be generated

## BUGS

**bold**, _italic_, [link](#BUGS)

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

https://github.com/utility-toolbox/roff
````
</details>

![example: manpage](https://github.com/utility-toolbox/roff/blob/main/README.assets/example-manpage.png?raw=true)
