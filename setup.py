#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys; sys.path.append('./src')  # noqa
import setuptools
from roff import __author__, __version__, __description__, __license__


install_requires = ['markdown-it-py']

images_requires = ['pillow']
images_svg_requires = [*images_requires, 'cairosvg']
watch_requires = ['pypager']
all_requires = [images_requires, images_svg_requires, watch_requires]

extras_require = {
    'images': all_requires,
    'images-svg': all_requires,
    'watch': watch_requires,
    'all': all_requires,
}

setuptools.setup(
    name="roff",
    version=__version__,
    description=__description__,
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author=__author__,
    license=__license__,
    url="https://github.com/utility-toolbox/roff",
    project_urls={
        "Organisation Github": "https://github.com/utility-toolbox",
        "Homepage": "https://github.com/utility-toolbox/roff/",
        # "Documentation": "https://utility-toolbox.github.io/roff/",
        "Bug Tracker": "https://github.com/utility-toolbox/roff/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require=extras_require,
    # test_suite="tests",
    entry_points={
        "console_scripts": [
            "roff = roff.__main__:main"
        ]
    },
    data_files=[
        ("man/man1", ["docs/roff.1"]),
        ("man/man5", ["docs/roff.5"]),
    ],
)
