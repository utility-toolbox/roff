roff(1) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## SYNOPSIS

- $`roff [-h] [-v] {convert,template} ...`
- $`roff convert [-h] source [dest]`
- $`roff template [-h] dest`

## DESCRIPTION

python-based cli to convert markdown to the roff (man-pages) format.

> see roff(5) for more information about the file specification

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
- Images (rendered as braille-art)
- Horizontal-Rule

## OPTIONS

### $`roff convert`

> Converts markdown files to roff files

#### `source`:
Markdown file that should be parsed

#### `[dest]`:
Manpage file

### $`roff template`

> Generates a Markdown file that you can fill

#### `-y`, `--yes`:
Overwrite file if it exists

#### `dest`:
Target file that should be generated

## BUGS

https://github.com/utility-toolbox/roff/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

### Organisation:
https://github.com/utility-toolbox

### Repository:
https://github.com/utility-toolbox/roff
