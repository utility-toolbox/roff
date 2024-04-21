# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap
from . import __version__, __cli__


parser = ap.ArgumentParser(prog='roff', formatter_class=ap.ArgumentDefaultsHelpFormatter)
parser.set_defaults(__cmd__=parser.print_help)
parser.add_argument('-v', '--version', action='version', version='{}'.format(__version__))
subparsers = parser.add_subparsers()


template_parser = subparsers.add_parser('template')
template_parser.set_defaults(__cmd__=__cli__.template.__cmd__)
template_parser.add_argument('dest',
                             help="Target file that should be generated")


def main():
    args = vars(parser.parse_args())
    cmd = args.pop('__cmd__')
    cmd(**args)


if __name__ == '__main__':
    main()
