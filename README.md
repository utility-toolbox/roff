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
pip install roff[front-matter]  # support for front-matter to configure roff
pip install roff[images]  # support for images
pip install roff[images-svg]  # support for svg-images
pip install roff[watch]  # support for rendering and auto-reloading a manpage while writing
```

> [!TIP] 
> After the installation you should be able to see [roff's manpage](https://github.com/utility-toolbox/roff/blob/main/docs/roff.1.md) with `man roff`
> or the file format information with `man roff.5`.

## Usage/Execution

> For more details inspect the manpage (`man roff.1`) to see all commands with their options.

For the common usage you can create a template markdown file with the `roff template` subcommand and then convert it to the roff-file-format with `roff convert`.

```shell
roff --help
roff template command.1.md
roff convert command.1.md
man ./command.1
```

Additionally, if `roff[watch]` was installed, you can run `roff watch` to see the rendered file that automatically re-renders if the file-content changes.

```shell
# shell 1
$ roff watch command.1.md
# shell 2
$ nano command.1.md
$ vim command.1.md
```

Additionally, if your project uses python `argparse.ArgumentParser` then you can start quicker by using the `roff from-parser` command instead of `roff template`.
This works almost like the template command, but fills most of the fields.

> [!WARNING]
> `from-parser` will import the parser from your specified file/module. Which means that the code will be run! Use with care!

```shell
$ roff from-parser --root src/ --output prog.1.md myprog.__main__:parser
```


## File Format

> For more details inspect the manpage (`man roff.5`) to see all file specifications.

`roff` uses markdown as the file format. It supports all commonmark markdown features (h1 is reserved for the head).

Additionally, roff brings 1 own markdown-feature, the `inline-command`!
By prepending your inline-code with a `$` sign it gets recognised as an inline-command and rendered in a more special way.

```markdown
$`command subcommand [--arg value] file...`
```

![example: inline-command](README.assets/example-inline-command.png)

> [!TIP]
> Use `roff template command.1.md` to get a pre-filled markdown file as a starting point.

## Configuration

Roff has multiple configuration options for a more customized experience.
Details about these options can be inspected via the manpage (`man roff.1`).
These options are only needed for a fine-tuned experience. For most users roff should work out of the box.

## Example

The following image shows the manpage of roff itself.

<small>(The manpage-content might be slightly outdated but still shows what roff can do)</small>

![example: manpage](https://github.com/utility-toolbox/roff/blob/main/README.assets/roff-manpage.png?raw=true)
