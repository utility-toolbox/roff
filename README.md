# roff
python-based cli to convert markdown to the roff (man-pages) format

<!-- TOC -->
* [roff](#roff)
  * [Installation](#installation)
  * [Usage/Execution](#usageexecution)
  * [Example](#example)
<!-- TOC -->

## Installation

[![PyPI - Version](https://img.shields.io/pypi/v/roff)
](https://pypi.org/project/roff/)

```shell
pip install roff
```

> Tip: after the installation you should be able to see [roff's manpage](https://github.com/utility-toolbox/roff/blob/main/docs/roff.1.md) with `man roff` 

## Usage/Execution

```shell
roff --help
roff template command.1.md
roff convert command.1.md
man ./command.1
```

## Example

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

![example-manpage](https://github.com/utility-toolbox/roff/blob/main/README.assets/example-manpage.png?raw=true)
