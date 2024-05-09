roff(1) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## SYNOPSIS

- $`roff [-h] [-v] {convert,template,tree,watch} ...`
- $`roff convert [-h] source [dest]`
- $`roff template [-h] dest`
- $`roff tree [-h] [--show-text | --no-show-text] source`
- $`roff watch [-h] source`

## DESCRIPTION

python-based cli to convert markdown to the roff (man-pages) format.

> see **roff(5)** for more information about the file specification.

Support for all* Markdown features:

> *h1 is reserved for the head.

- heading (h2-h6)
- Ordered Lists
- Unordered Lists
- Code-Blocks
- Inline
  - Code
  - Bold
  - Emphasis
  - Links
- Images (rendered as braille-art | requires `roff[images]`)
- Horizontal-Rule

## OPTIONS

$`roff [-h] [-v] {convert,template,tree,watch} ...`

### $`roff convert`

> Converts markdown files to roff files

$`roff convert [-h] source [dest]`

* `source`:
Markdown file that should be parsed

* `[dest]`:
Manpage file

### $`roff template`

> Generates a Markdown file that you can fill

$`roff template [-h] dest`

* `-y`, `--yes`:
Overwrite file if it exists

* `dest`:
Target file that should be generated

### $`roff tree`

> Shows the parsed tree-structure of a markdown document. (For debugging purposes)

$`roff tree [-h] [--show-text | --no-show-text] source`

* $`--show-text`, $`--no-show-text`:
Shows text content in the tree

* `source`:
Markdown file that should be parsed

### $`roff watch`

> Start the manpage while automatically updating it. (experimental)

$`roff watch [-h] source`

* `source`:
Markdown file that should be parsed

#### warning:

This feature can be a bit buggy and require you to close your terminal.

## BUGS

https://github.com/utility-toolbox/roff/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

### Organisation:
https://github.com/utility-toolbox

### Repository:
https://github.com/utility-toolbox/roff
