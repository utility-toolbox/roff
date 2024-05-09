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
from ._util import *
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

    # yes. I know that 80 won't fit the default terminal size of 80 because the section offset
    width: int = int(os.getenv('ROFF_WIDTH', 80))
    ascii: bool = os.getenv('ROFF_ASCII', "no").lower() in {"yes", "true", "1"}

    def __init__(self, fp: t.Union[str, os.PathLike]) -> None:
        self._stream = io.StringIO()
        self._had_head = False
        self._fp = Path(fp).absolute()
        self._root = self._fp.parent

        self.manpage_area = 1  # default. should be overwritten while parsing

        parser = get_parser()

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
            raise SyntaxError(f"First element in the document should be the header. (got {node.type})")
        parser = getattr(self, f"_parse_{node.tag}", None)
        if parser is None:
            warnings.warn(f"Unsupported node tag '{node.tag}' of type '{node.type}'", RuntimeWarning)
            return
        parser(node)

    def _render_inline(self, node: markdown_it.tree.SyntaxTreeNode) -> str:
        chunks = []

        for child in node.children:
            if child.type == 'text':
                chunks.append(escape(child.content))
            elif child.type == 'code_inline':
                chunks.append(f'\\fI{child.content}\\fP')
            elif child.type == 'strong':
                chunks.append(f'\\fB{self._render_inline(node=child)}\\fP')
            elif child.type == 'em':
                chunks.append(f'\\fI{self._render_inline(node=child)}\\fP')
            elif child.type == 'softbreak':
                chunks.append(' ')
            elif child.type == 'hardbreak':
                chunks.append('\n.br\n')
            elif child.type == 'link':
                href = child.attrGet('href')
                text = self._render_inline(node=child)
                if href == text:
                    chunks.append(text)
                else:
                    chunks.append(f'\n.UR {href}\n{text}\n.UE')
            elif child.type == 'image':
                href = child.attrGet('src')
                hyperref_re = re.compile(r'^\w+://')  # checks for http://, https://, data://, file://
                if hyperref_re.match(href) is None:  # relative path to a file
                    href = f'file://{self._root.joinpath(href).absolute()}'  # make it absolute to our root directory
                braille = render_image(url=href, max_dimensions=(self.width, self.width * 3))
                content = textwrap.indent(braille, '.br\n')  # ensure line-wraps
                chunks.append(f'.sp\n{content}\n.sp\n')
            elif child.type == 'command_inline':  # custom through plugin
                chunks.append(self._render_inline_command(command=child.content))
            else:
                warnings.warn(f"Unsupported inline node tag '{child.tag}' of type '{child.type}'", RuntimeWarning)

        return ''.join(chunks)

    @staticmethod
    def _render_inline_command(command: str) -> str:
        command = command.strip()

        def repl(match: re.Match) -> str:
            head = match.group('head')
            if head is not None:
                return f'\\fB{escape(head)}\\fP'
            argkey = match.group('argkey')
            if argkey:
                argvalue = match.group('argvalue')
                if argvalue:
                    return f'[\\fB{escape(argkey)}\\fP \\fI{escape(argvalue)}\\fP]'
                else:
                    return f'[\\fB{escape(argkey)}\\fP]'
            argument = match.group()
            if argument.startswith("-"):
                return f'\\fB{escape(argument)}\\fP'
            else:
                return f'\\fI{escape(argument)}\\fP'

        patterns_re = re.compile(r'^(?P<head>\w[\w\-]*)'  # ^command
                                 r'|\[(?P<argkey>--?\w[\w-]*)(?: (?P<argvalue>\w[\w\-]*))?]'  # [--key value]
                                 r'|(?<!\\)(?P<quote>[\"\']).*?(?<!\\)(?P=quote)'  # "longer text's"
                                 r'|(-{0,2}\w[\w\-]*)')  # other stuff

        return patterns_re.sub(repl, command)

    def _parse_h1(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        from datetime import date

        if self._had_head:
            raise SyntaxError("Duplicate Head detected")
        self._had_head = True

        head_re = re.compile(r'^(?P<command>\w+)\\?\((?P<manpage_area>\d)\\?\) \\?-\\?- (?P<description>.+)$')
        content = self._render_inline(node=node.children[0])
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
        self._stream.write(f'\\fB{command}\\fP {"-" if self.ascii else "•"} {match.group("description")}\n')

    def _parse_h2(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.SH "{self._render_inline(node=node.children[0])}"\n')

    def _parse_h3(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.SS "{self._render_inline(node=node.children[0])}"\n')

    def _parse_h4(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        self._stream.write(f'.sp\n{self._render_inline(node=node.children[0])}\n.sp\n')

    # maybe not the best solution
    _parse_h5 = _parse_h4
    _parse_h6 = _parse_h4

    def _parse_p(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        content = self._render_inline(node=node.children[0])
        content = re.sub(r'\n{2,}', '\n.sp\n', content)
        if node.level == 0:
            self._stream.write('.P\n')
        self._stream.write(f'{content}\n')

    @staticmethod
    def _check_newline(text: str) -> bool:
        r""" checks the output of _render_inline if it won't fit into one line """
        return (
            # len(text) >= self.width  # won't fit in one line (good in theory. bad in praxis)
            '\n.br\n' in text  # line-break
            or '\n.sp\n' in text  # vertical space
        )

    def _check_inline_text_list(self, node: markdown_it.tree.SyntaxTreeNode) -> bool:
        r""" Better do not touch this function. It's a mess. But at least it works """
        assert node.tag in {'ul', 'ol'}
        return all((
            (len(li.children)  # any children
             and li.children[0].type == 'paragraph'  # first is paragraph
             and len(li.children[0].children) == 1  # with one child
             and li.children[0].children[0].type == 'inline'  # which is inline
             and not self._check_newline(
                        self._render_inline(node=li.children[0].children[0])  # and not over multiple lines
            )) for li in node.children
        ))

    def _parse_ul(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        r""" unordered list """
        deep = node.level > 0
        self._stream.write('.br\n' if deep else '.sp\n')
        bullet = '*' if self.ascii else '•'
        if self._check_inline_text_list(node=node):
            for list_item in node.children:
                head, *body = list_item.children
                self._stream.write(f'{bullet} {self._render_inline(head.children[0])}\n.br\n')
                if body:
                    self._stream.write('.RS 2\n')
                    self._parse_children(children=body)
                    self._stream.write('.RE\n')
        else:
            for list_item in node.children:
                self._stream.write(f'{bullet}\n.RS 2\n')
                self._parse_children(children=list_item.children)
                self._stream.write(f'.RE\n')
        self._stream.write('.br\n' if deep else '.sp\n')

    def _parse_ol(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        r""" ordered list """
        deep = node.level > 0
        self._stream.write('.br\n' if deep else '.sp\n')
        if self._check_inline_text_list(node=node):
            for i, list_item in enumerate(node.children):
                head, *body = list_item.children
                self._stream.write(f'{i+1}. {self._render_inline(head.children[0])}\n.br\n')
                if body:
                    self._stream.write('.RS 2\n')
                    self._parse_children(children=body)
                    self._stream.write('.RE\n')
        else:
            for i, list_item in enumerate(node.children):
                self._stream.write(f'{i+1}.\n.RS 2\n')
                self._parse_children(children=list_item.children)
                self._stream.write(f'.RE\n')
        self._stream.write('.br\n' if deep else '.sp\n')

    def _parse_blockquote(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        # todo: prefix each line with '|' somehow
        self._stream.write(f'.sp\n.RS 2\n')
        self._parse_children(children=node.children)
        self._stream.write(f'.RE\n.sp\n')

    def _parse_code(self, node: markdown_it.tree.SyntaxTreeNode) -> None:
        content = node.content.expandtabs(4).strip()
        content = textwrap.dedent(content)  # left-align
        if node.info in {'', 'text', 'txt'}:  # print with left-offset
            content = re.sub(r'\n{2,}', '\n.sp\n', escape(content))
            content = textwrap.indent(content, prefix='.br\n')  # ensures newlines
            self._stream.write(f'.sp\n.RS 2\n.EX\n\\fI\n{content}\n\\fP\n.EE\n.RE\n.sp\n')
        else:  # prints with line-numbers
            self._stream.write(f'.sp\n')
            lines = content.splitlines()
            num_width = len(lines) // 10
            for i, line in enumerate(lines):
                self._stream.write(f'{str(i+1).rjust(num_width)} | \\fI{escape(line)}\\fP\n.br\n')
            self._stream.write(f'.sp\n')

    def _parse_hr(self, _node: markdown_it.tree.SyntaxTreeNode) -> None:
        character = "-" if self.ascii else "━"
        self._stream.write(f".sp\n{character * self.width}\n.sp\n")
