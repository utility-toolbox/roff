# -*- coding=utf-8 -*-
r"""

"""
import markdown_it.tree
from .._util import get_parser


def __cmd__(source: str, *, show_text: bool = False):
    with open(source, 'r') as file:
        markdown = file.read()

    parser = get_parser()
    tokens = parser.parse(src=markdown)
    nodes = markdown_it.tree.SyntaxTreeNode(tokens, create_root=True)
    print(nodes.pretty(indent=2, show_text=show_text))
