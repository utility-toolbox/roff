# -*- coding=utf-8 -*-
r"""
python-based cli to convert markdown to the roff (man-pages) format
"""
import argparse as ap
from . import __version__, __cli__


parser = ap.ArgumentParser(prog='roff', formatter_class=ap.ArgumentDefaultsHelpFormatter, description=__doc__)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version='{}'.format(__version__))
parser.add_argument('--list-areas', action=__cli__.util.ActionListManpageAreas,
                    help="Lists the manpage-areas and exit")
subparsers = parser.add_subparsers()


convert_parser = subparsers.add_parser('convert',
                                       help="Converts markdown files to roff files")
convert_parser.set_defaults(__cmd__=__cli__.convert.__cmd__)
convert_parser.add_argument('source',
                            help="Markdown file that should be parsed")
convert_parser.add_argument('dest', nargs=ap.OPTIONAL,
                            help="Manpage file that should be generated")


template_parser = subparsers.add_parser('template',
                                        help="Generates a Markdown file that you can fill")
template_parser.set_defaults(__cmd__=__cli__.template.__cmd__)
template_parser.add_argument('-y', '--yes', action='store_true',
                             help="Overwrite file if it exists")
template_parser.add_argument('dest',
                             help="Target file that should be generated")


tree_parser = subparsers.add_parser('tree',
                                    help="Shows the parsed tree-structure of a markdown document."
                                         " (For debugging purposes)")
tree_parser.set_defaults(__cmd__=__cli__.tree.__cmd__)
tree_parser.add_argument('--show-text', action=ap.BooleanOptionalAction,
                         help="Show text in the tree")
tree_parser.add_argument('source',
                         help="Markdown file that should be parsed")


watch_parser = subparsers.add_parser('watch',
                                     help="Start the manpage while automatically updating it. (experimental)")
watch_parser.set_defaults(__cmd__=__cli__.watch.__cmd__)
watch_parser.add_argument('source',
                          help="Markdown file that should be parsed")


def main():
    args = vars(parser.parse_args())
    cmd = args.pop('__cmd__')
    cmd(**args)


if __name__ == '__main__':
    main()
