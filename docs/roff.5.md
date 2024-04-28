roff(5) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## DESCRIPTION

see roff(1) for more information about the CLI.

This document is about the .md file-specification

> Use $`roff template command.1.md` to get a template as a starting point.

## FILES

Input files should follow the naming convention of `[command].[area].md` (e.g. `roff.1.md`)

Output files should follow the naming convention of `[command].[area]` (e.g. `roff.1`)

## ELEMENTS

### Document Head

The Document head should have the following structure and is required in the document

```markdown
command(1) -- description
=============================================
```

> Because h1 is reserved for the head you are not allowed to use `#` in your files
> 
> ```markdown
> # SECTION
> ```

### Sections

```markdown
## SECTION
```

### Subsections

```markdown
### SUBSECTION
```

### Subsubsections

```markdown
#### SUBSUBSECTION
##### SUBSUBSECTION
###### SUBSUBSECTION
```

### Unordered Lists

```markdown
- First Element
- Second Element
```

### Ordered Lists

```markdown
1. First Element
2. Second Element
```

### Blockquotes

```markdown
> You can simply add blockquotes by starting a line with `>`
```

### Code-Blocks

````markdown
```
code-content
```
````

### Inline/Text

```markdown
You can add `inline-code`, **bold** and *italic* code from markdown which are displayed in their own way
```

### Links

```markdown
Links are possible as reference (e.g. roff(1)) or via the markdown syntax (e.g. [repository](https://github.com/utiltiy-toolbox/roff))
```

### Images

requires `roff[images]` or `roff[images-svg]`

```markdown
![alt](asset.png)
![alt](https://server.com/asset.png)
```

### Separator

```markdown
---
```

## NOTES


## EXAMPLE

````markdown
command(1) -- @DESCRIPTION
=============================================

## DESCRIPTION

## OPTIONS

### `subcommand`

#### `-h`, `--help`:
shows a help message and exists
````

## BUGS

https://github.com/utility-toolbox/roff/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

### Organisation
https://github.com/utility-toolbox

### Repository
https://github.com/utility-toolbox/roff
