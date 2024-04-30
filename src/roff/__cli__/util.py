# -*- coding=utf-8 -*-
r"""

"""
import argparse as ap


class ActionListManpageAreas(ap.Action):
    def __init__(self, option_strings, dest, help=None, metavar=None):
        super().__init__(option_strings=option_strings, nargs=0, help=help, metavar=metavar,
                         dest=ap.SUPPRESS, default=ap.SUPPRESS)

    def __call__(self, parser: ap.ArgumentParser, *args, **kwargs):
        print("1. general commands")
        print("2. system calls")
        print("3. library functions")
        print("4. special files")
        print("5. file formats and conventions")
        print("6. games and screensavers")
        print("7. miscellanea")
        print("8. system administration commands and daemons")
        parser.exit(0)
