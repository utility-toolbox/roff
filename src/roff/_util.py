# -*- coding=utf-8 -*-
r"""

"""
import re
import markdown_it


__all__ = ['get_parser', 'escape']


def get_parser() -> 'markdown_it.MarkdownIt':
    from ._markdown import markdown_plugin_command, markdown_plugin_front_matter

    parser = markdown_it.MarkdownIt()
    parser.use(markdown_plugin_command)
    parser.use(markdown_plugin_front_matter)
    return parser


ESCAPE_RULES = {
    re.compile(r'\\'): r"\\\\",  # backslash
    re.compile(r'\''): r"\\[aq]",  # apostrophe
    re.compile(r'\"'): r"\\[dq]",  # double-quotation
    re.compile(r'(?<=\d)-(?=\d)'): r"\\[en]",  # en-dash
    re.compile(r'(?<=\w)-(?=\w)'): r"\\[em]",  # em-dash
    re.compile(r'`'): r"\\[ga]",  # grave accent
    re.compile(r'\^'): r"\\[ha]",  # circumflex accent
    re.compile(r'~'): r"\\[ti]",  # tilde
    re.compile(r'-'): r"\\-",  # minus sign
}


def escape(text: str) -> str:
    for rule, replacement in ESCAPE_RULES.items():
        text = rule.sub(replacement, text)
    return text
