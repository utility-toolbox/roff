roff(1) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## SYNOPSIS

- `roff [-h] [-v] {convert,template} ...`
- `roff convert [-h] source [dest]`
- `roff template [-h] dest`

## DESCRIPTION

python-based cli to convert markdown to the roff (man-pages) format.

Supported Markdown Features:
- heading (h2-h4) (h1 is reserved for the head)
- Flat Lists
- code-blocks
- inline-code
- inline-bold
- inline-italic

## OPTIONS

### `convert`

> Converts markdown to roff

#### `source`:
Markdown file that should be parsed

#### `[dest]`:
Manpage file

### `template`

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
