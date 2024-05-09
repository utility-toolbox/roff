# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from pathlib import Path
from ..convert import Converter


def __cmd__(source: str, dest: t.Optional[str]) -> None:
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"Input file {source!s} does not exist")

    converter = Converter(fp=source)

    if dest is None:
        dest = source.with_suffix('').with_suffix(f".{converter.manpage_area}")
    else:
        dest = Path(dest)

    with open(dest, 'w') as file:
        file.write(converter.getvalue())
