# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import argparse as ap
from pathlib import Path
from .from_parser import __cmd__ as from_parser


__all__ = ['__cmd__']


def __cmd__(output: t.TextIO) -> None:
    command = output.name.split('.', 1)[0]
    if command == '<stdout>':
        command = "@COMMAND"
    manpage_area = next((int(sfx[1]) for sfx in Path(output.name).suffixes if sfx[1:].isdigit() and len(sfx) == 2), 1)

    parser = ap.ArgumentParser(prog=command, epilog="@DESCRIPTION", add_help=True)
    parser.manpage_area = manpage_area

    from_parser(root=".", output=output, parser=parser)
