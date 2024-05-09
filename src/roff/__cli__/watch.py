# -*- coding=utf-8 -*-
r"""

"""
import time
import tempfile
import traceback
import subprocess as sp
from pathlib import Path
from ..convert import convert


def __cmd__(source: str):
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"Input file {source!s} does not exist")

    def render_source() -> str:
        try:
            return convert(fp=source)
        except SyntaxError as error:
            return '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))

    def update_tmpfile(new: str) -> None:
        tmp.truncate(0)
        tmp.write(new)
        tmp.flush()

    with tempfile.NamedTemporaryFile('w+') as tmp:
        last_mtime = source.stat().st_mtime_ns
        content = render_source()
        update_tmpfile(content)
        pager_process = sp.Popen(['man', tmp.name])

        while pager_process.poll() is None:
            time.sleep(0.1)

            current_mtime = source.stat().st_mtime_ns
            if last_mtime != current_mtime:
                last_mtime = current_mtime

                pager_process.terminate()
                content = render_source()
                update_tmpfile(content)
                pager_process.wait()  # ensure pager_process died
                pager_process = sp.Popen(['man', tmp.name])
