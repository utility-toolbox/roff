# -*- coding=utf-8 -*-
r"""

"""
import os
import io
import re
import textwrap
import warnings
import typing as t
import markdown_it.tree
from . import __version__


__all__ = ['convert', 'Converter']


def convert(source: str) -> str:
    r"""
    converts markdown to roff

    :param source: markdown file content
    :return: roff file content
    """
    return Converter(source).getvalue()


class Converter:
    _stream: io.StringIO
    _had_head: bool
    manpage_area: int

    def __init__(self, source: str) -> None:
        self._stream = io.StringIO()
        self._had_head = False

        self.manpage_area = 1  # default. should be overwritten

        parser = markdown_it.MarkdownIt()

        tokens = parser.parse(src=source)
        root_node = markdown_it.tree.SyntaxTreeNode(tokens=tokens, create_root=True)

        self._add_head()
        # print(root_node.pretty(show_text=True))
        self._parse_children(children=root_node.children)
        if not self._had_head:
            raise SyntaxError("Missing head")

    def getvalue(self) -> str:
        return self._stream.getvalue()

    def _add_head(self):
        self._stream.write(f".\\\" generated with roff/v{__version__}\n")
        self._stream.write(f".\\\" https://pypi.org/project/roff/{__version__}\n")
        self._stream.write(f".\\\" https://github.com/utility-toolbox/roff/\n")
        self._stream.write(f".\\\"\n")

    def _parse_children(self, children: t.List[markdown_it.tree.SyntaxTreeNode]) -> None:
        for child in children:
            self._parse_node(node=child)

    def _parse_node(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        if not self._had_head and node.tag != 'h1':
            raise SyntaxError("First element in the document should be the header")
        parser = getattr(self, f"_parse_{node.tag}", None)
        if parser is None:
            warnings.warn(f"Unsupported node tag '{node.tag}' of type '{node.type}'", RuntimeWarning)
            return
        parser(node=node)

    def _parse_inline(self, node: markdown_it.tree.SyntaxTreeNode) -> str:
        chunks = []

        for child in node.children:
            if child.type == 'text':
                chunks.append(escape(child.content))
            elif child.type == 'code_inline':
                chunks.append(f'\\fB{child.content}\\fP')
            elif child.type == 'strong':
                chunks.append(f'\\fB{self._parse_inline(node=child)}\\fP')
            elif child.type == 'em':
                chunks.append(f'\\fI{self._parse_inline(node=child)}\\fR')
            elif child.type == 'softbreak':
                chunks.append('\n.br\n')
            elif child.type == 'hardbreak':
                chunks.append('\n.br\n.br\n')
            elif child.type == 'link':
                href = child.attrGet('href')
                text = self._parse_inline(node=child)
                if href == text:
                    chunks.append(escape(text))
                else:
                    chunks.append(f'\n.UR {href}\n{escape(text)}\n.UE')
            # elif child.type == 'image':
            #     pass  # todo: `pip install roff[image]` with Pillow
            else:
                warnings.warn(f"Unsupported inline node tag '{child.tag}' of type '{child.type}'", RuntimeWarning)

        return ''.join(chunks)

    def _parse_h1(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        from datetime import date

        if self._had_head:
            raise SyntaxError("Duplicate Head detected")
        self._had_head = True

        head_re = re.compile(r'^(?P<command>\w+)\\?\((?P<manpage_area>\d)\\?\) \\?-\\?- (?P<description>.+)$')
        content = self._parse_inline(node=node.children[0])
        match = head_re.search(content)
        if match is None:
            raise SyntaxError("Unsupported format of head. (expected 'command(1) -- description')")

        command = match.group('command')
        self.manpage_area = area = match.group('manpage_area')

        # Congratulations. This part is not documented.
        # You are probably here to hide this advertisement. Because I'm generous I'll make it easy for you
        ad_url = "" if os.getenv('ROFF_NO_ADD') == 'yes' else "github.com/utility-toolbox/roff"
        self._stream.write(f'.TH "{command.upper()}" "{area}" "{date.today():%d %B %Y}" "{ad_url}"\n')
        self._stream.write(f'.SH "NAME"\n')
        self._stream.write(f'\\fB{command}\\fP \\- {match.group("description")}\n')

    def _parse_h2(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.SH "{self._parse_inline(node=node.children[0])}"\n')

    def _parse_h3(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.SS "{self._parse_inline(node=node.children[0])}"\n')

    def _parse_h4(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.sp\n{self._parse_inline(node=node.children[0])}\n.br\n')

    def _parse_p(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        content = self._parse_inline(node=node.children[0])
        if not content.strip():
            return
        content = re.sub(r'\n{2,}', '\n.\n', content)
        self._stream.write(f'{content}\n')

    def _parse_ul(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        r""" unordered list """
        self._stream.write('.br\n')
        for child in node.children:
            self._stream.write(f'*\n.RS 2\n')
            self._parse_children(children=child.children)
            self._stream.write(f'.RE\n')
        self._stream.write('.br\n')

    def _parse_ol(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        r""" ordered list """
        self._stream.write('.br\n')
        for i, child in enumerate(node.children):
            self._stream.write(f'{i+1}.\n.RS 2\n')
            self._parse_children(children=child.children)
            self._stream.write(f'.RE\n')
        self._stream.write('.br\n')

    def _parse_blockquote(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.sp\n.RS 2\n')
        self._parse_children(children=node.children)
        self._stream.write(f'.RE\n.sp\n')

    def _parse_code(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        content = re.sub(r'\n{2,}', '\n.sp\n', node.content.expandtabs(4).strip())
        content = textwrap.dedent(content)  # left-align
        content = textwrap.indent(content, prefix='.br\n')  # ensures newlines
        self._stream.write(f'.sp\n.RS 2\n\\fI\n{content}\n\\fR\n.RE\n.sp\n')


def escape(text: str, *, _escapes: str = '"\'.\\') -> str:
    return text.translate(str.maketrans({
        c: f"\\{c}"
        for c in _escapes
    }))
