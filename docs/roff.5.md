roff(5) -- python-based cli to convert markdown to the roff (man-pages) format
=============================================

## DESCRIPTION

see roff(1) for more information about the CLI.

This document is about the .md file-specification

> Use $`roff template 'command.1.md'` or $`roff from-parser 'file.py:arg_parser'` to get a template as a starting point.


## CONFIGURATION

There are two ways to configure the behavior of roff.
For more detailed information about the options see the ENVIRONMENT section in roff(1).

### With Environment Variables

The first option is to set environment variables. These variables are prefixed with `ROFF_` (e.g. `ROFF_WIDTH`).

### With Front-Matter

The second option is to add a [front-matter](#front-matter) to your document.

e.g.

```markdown
---
width: 60
---
command(1) -- description
=========================
```

## FILES

Input files should follow the naming convention of `[command].[area].md` (e.g. `roff.1.md`)

Output files should follow the naming convention of `[command].[area]` (e.g. `roff.1`)

## ELEMENTS

### Front-Matter

The Front-Matter is used to [configure `roff`'s behavior](#configuration).

In order to add a front-matter you have to place it at the start of your document.
The Front-Matter starts and ends with a `---`.
Everything in between is yaml.

```markdown
---
width: 60
---
command(1) -- description
=========================
```

### Document Head

The Document head should have the following structure and is required in the document

```markdown
command(1) -- description
=============================================
```

> Because h1 is reserved for the head you are not allowed to use `#` in your files.
> e.g.
> ```markdown
> # SECTION
> ```

### Sections

If you want to add a section you should use conventional section names. (e.g. `NAME`, `CONFIGURATION`, `DESCRIPTION`)

The section name should also be in uppercase.

```markdown
## SECTION
```

### Subsections

You are free to label them as you like.

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

- First Element
- Second Element

```markdown
- First Element
- Second Element
```

### Ordered Lists

1. First Element
2. Second Element

```markdown
1. First Element
2. Second Element
```

### Blockquotes

> You can simply add blockquotes by starting a line with `>`. This will indent the block slightly.

```markdown
> You can simply add blockquotes by starting a line with `>`. This will indent the block slightly.
```

### Code-Blocks

````markdown
```
code-content
```
````

### Inline/Text

You can add `inline-code`, **bold** and *italic* code from markdown which are displayed in their own way

```markdown
You can add `inline-code`, **bold** and *italic* code from markdown which are displayed in their own way
```

### Links

Links are possible as reference (e.g. roff(1)) or via the markdown syntax (e.g. [repository](https://github.com/utiltiy-toolbox/roff))

```markdown
Links are possible as reference (e.g. roff(1)) or via the markdown syntax (e.g. [repository](https://github.com/utiltiy-toolbox/roff))
```

### Images

In order to render image, roff requires to be installed with `roff[images]`, `roff[images-svg]` or `roff[all]`.

```markdown
![alt](asset.png)
![alt](https://server.com/asset.png)
```

### Separator

---

```markdown
---
```

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
<https://github.com/utility-toolbox/roff/issues>

## AUTHOR
<https://github.com/Barakudum>

## SEE ALSO

### Other Man-Pages
roff(1)

### Organisation
<https://github.com/utility-toolbox>

### Repository
<https://github.com/utility-toolbox/roff>
