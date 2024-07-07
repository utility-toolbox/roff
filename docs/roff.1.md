roff(1) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## SYNOPSIS

- $`roff [-h] [-v] {convert,from-parser,template,tree,watch} ...`
- $`roff convert [-h] source [dest]`
- $`roff from-parser [-h] [--root ROOT] [-o OUTPUT] parser`
- $`roff template [-h] output`
- $`roff watch [-h] source`
- $`roff tree [-h] [--show-text | --no-show-text] source` (debugging)

## DESCRIPTION

python-based cli to convert markdown to the roff (man-pages) format

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

Note: to specify the parser for an executable module use the format '`module[.submodule].__main__[:variable]`'.

## OPTIONS

$`roff [-h] [-v] [--list-areas] {convert,from-parser,template,tree,watch} ...`

* $`-h`, $`--help`:
show this help message and exit

* $`-v`, $`--version`:
show program's version number and exit

* $`--list-areas`:
Lists the manpage-areas and exit

### $`roff convert`

> Converts markdown files to roff files

$`roff convert [-h] source [dest]`

* $`-h`, $`--help`:
show this help message and exit

* $`source`:
Markdown file that should be parsed

* $`[dest]`:
Manpage file that should be generated

### $`roff from-parser`

$`roff from-parser [-h] [--root ROOT] [-o OUTPUT] parser`

* $`-h`, $`--help`:
show this help message and exit

* $`--root`:
Root directory to the search the module in

* $`-o`, $`--output`:
Output file name

* $`parser`:
Entrypoint-Specification to the parser. (Format: '`module[.submodule][:variable]`')

### $`roff template`

> Generates a Markdown file that you can fill

$`roff template [-h] output`

* $`-h`, $`--help`:
show this help message and exit

* `output`:
Target file that should be generated

### $`roff watch`

> Start the manpage while automatically updating it. (experimental)

$`roff watch [-h] source`

* $`-h`, $`--help`:
show this help message and exit

* `source`:
Markdown file that should be parsed

#### warning:

This feature can be a bit buggy and require you to close your terminal.

### $`roff tree`

> Shows the parsed tree-structure of a markdown document. (For debugging purposes)

$`roff tree [-h] [--show-text | --no-show-text] source`

* $`-h`, $`--help`:
show this help message and exit

* $`--show-text`, $`--no-show-text`:
Shows text content in the tree

* `source`:
Markdown file that should be parsed

## BUGS

https://github.com/utility-toolbox/roff/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

### Organisation:
https://github.com/utility-toolbox

### Repository:
https://github.com/utility-toolbox/roff
