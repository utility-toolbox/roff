# -*- coding=utf-8 -*-
r"""

"""
import io
import math
import typing as t
import urllib.request
import urllib.response
try:
    from PIL import Image
except ModuleNotFoundError:
    Image = None
try:
    import cairosvg
except ModuleNotFoundError:
    cairosvg = None


__all__ = ['render_image']


OFFSET = 0x2800

X0 = 0
L1 = 1
L2 = 2
L3 = 4
R1 = 8
R2 = 16
R3 = 32
L4 = 64
R4 = 128
OFFSETMAP = {
    (0, 0): L1,
    (0, 1): L2,
    (0, 2): L3,
    (0, 3): L4,
    (1, 0): R1,
    (1, 1): R2,
    (1, 2): R3,
    (1, 3): R4,
}


def render_image(url: str, max_dimensions: t.Tuple[int, int] = (80, 500)) -> str:
    r"""

    :param url: hyperref
    :param max_dimensions: in characters
    :return: as braille rendered image
    """
    if Image is None:
        raise RuntimeError("image rendering is not supported (`pip3 install roff[images]`)")

    max_width, max_height = max_dimensions
    response: urllib.response.addinfourl = urllib.request.urlopen(url=url, timeout=15)

    content_type = response.headers.get('content-type', None)
    if content_type is None:
        raise RuntimeError("missing content-type header")
    maintype, subtype = content_type.split('/', 1)

    if maintype != 'image':
        raise TypeError(f"unsupported content type: '{content_type}'")
    if subtype == 'svg+xml':
        if cairosvg is None:
            raise RuntimeError("svg-image rendering is not supported (`pip3 install roff[images-svg]`)")
        buffer = io.BytesIO()
        cairosvg.svg2png(file_obj=response, write_to=buffer, output_width=max_width)
        buffer.seek(0)
        response = buffer  # noqa

    with Image.open(response) as image:
        image.thumbnail((max_width * 2, max_height*4), resample=Image.Resampling.LANCZOS)  # limit size
        image = image.convert("1")  # make black and white

    n_rows = math.ceil(image.height / 4)
    n_columns = math.ceil(image.width / 2)

    lines: t.List[t.List[str]] = []

    for row in range(n_rows):
        characters: t.List[str] = []
        lines.append(characters)
        for col in range(n_columns):
            character = X0
            for off_y in range(4):
                for off_x in range(2):
                    rx, ry = (col * 2) + off_x, (row * 4) + off_y
                    try:
                        pixel = image.getpixel((rx, ry))
                    except IndexError:
                        pass
                    else:
                        if pixel:
                            character |= OFFSETMAP[(off_x, off_y)]
            characters.append(chr(OFFSET + character))

    return '\n'.join(''.join(character) for character in lines)
