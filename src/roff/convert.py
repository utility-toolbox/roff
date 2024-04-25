# -*- coding=utf-8 -*-
r"""

"""
import os
import io
import re
import textwrap
import warnings
import typing as t
from pathlib import Path
import markdown_it.tree
from . import __version__
from ._images import render_image


__all__ = ['convert', 'Converter']


def convert(fp: t.Union[str, os.PathLike]) -> str:
    r"""
    converts markdown to roff

    :param fp: markdown file to convert
    :return: roff file content
    """
    return Converter(fp).getvalue()


class Converter:
    _stream: io.StringIO
    _had_head: bool
    _fp: Path
    _root: Path
    manpage_area: int

    width: int = int(os.getenv('ROFF_WIDTH', 80))
    ascii: bool = os.getenv('ROFF_ASCII', "no").lower() in {"yes", "true", "1"}

    def __init__(self, fp: t.Union[str, os.PathLike]) -> None:
        self._stream = io.StringIO()
        self._had_head = False
        self._fp = Path(fp).absolute()
        self._root = self._fp.parent

        self.manpage_area = 1  # default. should be overwritten while parsing

        parser = markdown_it.MarkdownIt()

        with open(self._fp, 'r') as file:
            source = file.read()

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
        parser(node)

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
            elif child.type == 'image':
                href = child.attrGet('src')
                hyperref_re = re.compile(r'^\w+://')  # checks for http://, https://, data://, file://
                if hyperref_re.match(href) is None:  # relative path to a file
                    href = f'file://{self._root.joinpath(href).absolute()}'  # make it absolute to our root directory
                braille = render_image(url=href, max_dimensions=(self.width, self.width * 3))
                content = textwrap.indent(braille, '.br\n')  # ensure line-wraps
                self._stream.write(f'.sp\n{content}\n.sp\n')
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
        content = re.sub(r'\n{2,}', '\n.sp\n', content)
        self._stream.write(f'.P\n{content}\n')

    def _parse_ul(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        r""" unordered list """
        self._stream.write('.br\n')
        bullet = '*' if self.ascii else '•'
        for child in node.children:
            self._stream.write(f'{bullet}\n.RS 2\n')
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
        self._stream.write(f'.sp\n.RS 2\n.EX\n\\fI\n{content}\n\\fR\n.EE\n.RE\n.sp\n')

    def _parse_hr(self, _node: markdown_it.tree.SyntaxTreeNode) -> None:
        character = "-" if self.ascii else "━"
        self._stream.write(f".br\n{character * self.width}\n.br\n")


def escape(text: str, *, _escapes: str = '"\'.\\') -> str:
    return text.translate(str.maketrans({
        c: f"\\{c}"
        for c in _escapes
    }))
