# -*- coding=utf-8 -*-
r"""

"""
from pathlib import Path


__all__ = ['__cmd__']


def __cmd__(dest: str) -> None:
    dest = Path(dest)
    if not dest.parent.is_dir():
        raise NotADirectoryError(f"parent directory '{dest.parent!s}' does not exist")

    command = dest.name.split('.', 1)[0]
    manpage_area = next((int(sfx[1]) for sfx in dest.suffixes if sfx[1:].isdigit() and len(sfx) == 2), 1)

    with open(dest, 'w') as f:
        f.write(fr"""{command}({manpage_area}) -- @DESCRIPTION
=============================================

## SYNOPSIS


## DESCRIPTION


## OPTIONS


## BUGS


## AUTHOR


## SEE ALSO

""")
