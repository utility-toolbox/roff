# -*- coding=utf-8 -*-
r"""

"""
import io
import sys
import argparse
import textwrap
# noinspection PyUnresolvedReferences,PyProtectedMember
from argparse import _SubParsersAction as SubParsersAction, ArgumentParser
import importlib
import typing as t


SubParsersAction: t.Type[argparse.Action]
ADDITIONAL_SECTIONS: t.List[str] = ["CONFIGURATION", "ENVIRONMENT", "FILES", "VERSIONS", "NOTES", "EXAMPLE",
                                    "BUGS", "AUTHOR", "SEE ALSO"]


def __cmd__(root: str, output: t.TextIO, parser: t.Union[str, ArgumentParser]) -> None:
    if isinstance(parser, str):
        parser = load_parser(root=root, parser_spec=parser)
    parser: argparse.ArgumentParser

    stream = io.StringIO()

    subparsers: t.List[argparse.ArgumentParser] = find_subparsers(parser=parser)

    head_description = parser.description.strip().splitlines(keepends=False)[0] if parser.description else ''

    manpage_area = getattr(parser, 'manpage_area', 1)

    stream.write(f"{parser.prog}({manpage_area}) -- {head_description}\n")
    stream.write(f"{'=' * 45}\n")  # dunno why 45
    stream.write("\n")

    stream.write("## SYNOPSIS\n")
    stream.write("\n")
    for subparser in subparsers:
        stream.write(f"- $`{format_usage(subparser.format_usage())}`\n")
    stream.write("\n")

    stream.write("## DESCRIPTION\n")
    stream.write("\n")
    if parser.usage:
        stream.write(textwrap.dedent(parser.usage).strip() + "\n")
        stream.write("\n")
    if parser.description:
        stream.write(textwrap.dedent(parser.description).strip() + "\n")
        stream.write("\n")
    if parser.epilog:
        stream.write(textwrap.dedent(parser.epilog).strip() + "\n")
        stream.write("\n")

    stream.write("## OPTIONS\n")
    stream.write("\n")
    for subparser in subparsers:
        if len(subparsers) != 1:  # 1 means only main-parser. we assume no subparsers
            stream.write(f"### $`{subparser.prog}`\n")
            stream.write("\n")
        if subparser.description:
            description = textwrap.dedent(subparser.description).strip()
            stream.write(textwrap.indent(description, "> ") + "\n")
            stream.write("\n")
        stream.write(f"$`{format_usage(subparser.format_usage())}`\n")
        stream.write("\n")
        # noinspection PyProtectedMember
        for action in subparser._actions:
            action: argparse.Action
            if not action.option_strings and action.dest == argparse.SUPPRESS:
                continue
            elif action.option_strings:
                stream.write(f"* {', '.join(f'$`{opt}`' for opt in action.option_strings)}:\n")
            elif action.required:
                stream.write(f"* $`{action.dest}`:\n")
            else:
                stream.write(f"* $`[{action.dest}]`:\n")
            if action.help:
                stream.write(textwrap.dedent(action.help).strip() + "\n")
            stream.write("\n")

    for section in ADDITIONAL_SECTIONS:
        stream.write(f"## {section}\n")
        section_key = section.lower().replace(" ", "_")
        if hasattr(parser, section_key):
            stream.write(textwrap.dedent(getattr(parser, section_key)).strip() + "\n")
        else:
            stream.write("\n")
        stream.write("\n")

    output.write(stream.getvalue())


def load_parser(root: str, parser_spec: str) -> argparse.ArgumentParser:
    modname, qualname_seperator, qualname = parser_spec.partition(':')
    sys.path.insert(0, root)
    try:
        module = importlib.import_module(modname)
    except ModuleNotFoundError as error:
        print(f"Could not import {modname!r} ({error!s})", file=sys.stderr)
        sys.exit(1)
    finally:
        sys.path.pop(0)
    if qualname_seperator:
        try:
            module_parser = getattr(module, qualname)
        except KeyError as error:
            print(f"Failed to get parser {qualname!r} ({error!s})", file=sys.stderr)
            sys.exit(1)
    else:
        module_parser = next((v for v in vars(module).values() if isinstance(v, argparse.ArgumentParser)), None)
        if module_parser is None:
            print(f"Failed to auto-detect parser for {modname!r}", file=sys.stderr)
            sys.exit(1)

    return module_parser


def find_subparsers(parser: argparse.ArgumentParser) -> t.List[argparse.ArgumentParser]:
    queue: t.List[argparse.ArgumentParser] = [parser]
    subparsers: t.List[argparse.ArgumentParser] = []

    while queue:
        current = queue.pop()
        subparsers.append(current)

        # noinspection PyProtectedMember
        parser_actions: t.List[argparse.Action] = current._actions
        subparser_action: t.Optional[SubParsersAction] = next(
            (action for action in parser_actions
             if isinstance(action, SubParsersAction)),
            None,
        )

        if subparser_action is not None:
            # noinspection PyUnresolvedReferences
            queue.extend(subparser_action.choices.values())

    return sorted(subparsers, key=lambda sp: sp.prog)


def format_usage(usage: str) -> str:
    import re
    return re.sub(r'\n\s+', ' ', usage).strip().removeprefix("usage: ")
