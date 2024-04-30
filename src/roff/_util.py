# -*- coding=utf-8 -*-
r"""

"""
import typing as t
if t.TYPE_CHECKING:
    from markdown_it import MarkdownIt


__all__ = ['get_parser', 'escape']


def get_parser() -> 'MarkdownIt':
    import markdown_it
    from ._markdown import markdown_plugin_command

    parser = markdown_it.MarkdownIt()
    parser.use(markdown_plugin_command)
    return parser


def escape(text: str, *, _escapes: str = '"\'.\\') -> str:
    return text.translate(str.maketrans({
        c: f"\\{c}"
        for c in _escapes
    }))
