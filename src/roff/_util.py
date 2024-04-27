# -*- coding=utf-8 -*-
r"""

"""


__all__ = ['escape']


def escape(text: str, *, _escapes: str = '"\'.\\') -> str:
    return text.translate(str.maketrans({
        c: f"\\{c}"
        for c in _escapes
    }))
