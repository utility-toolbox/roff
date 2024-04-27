# -*- coding=utf-8 -*-
r"""

"""
from pathlib import Path


__all__ = ['__cmd__']


def __cmd__(dest: str, *, yes: bool) -> None:
    dest = Path(dest)
    if not dest.parent.is_dir():
        raise NotADirectoryError(f"parent directory '{dest.parent!s}' does not exist")
    if dest.is_file() and not yes:
        response = input(f"'{dest!s}' already exists. Do you want to overwrite it? [Y/n] ")
        if response.lower() not in {'y', 'yes'}:
            exit(0)

    command = dest.name.split('.', 1)[0]
    manpage_area = next((int(sfx[1]) for sfx in dest.suffixes if sfx[1:].isdigit() and len(sfx) == 2), 1)

    with open(dest, 'w') as f:
        f.write(fr"""{command}({manpage_area}) -- @DESCRIPTION
=============================================

## SYNOPSIS

- $`{command} [-h]`

## DESCRIPTION


## OPTIONS

<!--
### `{command} <SUBCOMMAND>`
-->

* `-h`, `--help`:
show the help message and exits

## CONFIGURATION


## ENVIRONMENT


## FILES


## VERSIONS


## NOTES


## EXAMPLE


## BUGS


## AUTHOR


## SEE ALSO

""")
