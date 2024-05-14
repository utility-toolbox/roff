# -*- coding=utf-8 -*-
r"""

"""
import time
import tempfile
import threading
import traceback
import subprocess
from pathlib import Path
import pypager
from ..convert import convert


def __cmd__(source: str):
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(f"Input file {source!s} does not exist")

    def update_looped():
        nonlocal last_mtime

        while not quitting.is_set():
            time.sleep(0.1)

            current_mtime = source.stat().st_mtime_ns
            if last_mtime != current_mtime:
                last_mtime = current_mtime
                sync_file_to_pager()

    def sync_file_to_pager():
        content = render_source()
        update_tmpfile_content(content)
        update_pager_source(render_tmpfile_with_man())

    def render_source() -> str:
        try:
            return convert(fp=source)
        except SyntaxError as error:
            return '\n'.join(traceback.format_exception(type(error), error, error.__traceback__))

    def update_tmpfile_content(new: str) -> None:
        tmp.truncate(0)
        tmp.seek(0)
        tmp.write(new)
        tmp.flush()

    def render_tmpfile_with_man() -> str:
        return subprocess.check_output(['man', tmp.name], text=True)

    def update_pager_source(new: str):
        pager.remove_current_source()
        pager.add_source(pypager.StringSource(new))
        pager.application.invalidate()

    with tempfile.NamedTemporaryFile('w+') as tmp:
        last_mtime = source.stat().st_mtime_ns

        quitting = threading.Event()
        update_thread = threading.Thread(target=update_looped)
        update_thread.start()

        pager = pypager.Pager()
        pager.add_source(pypager.StringSource(""))  # 0 index buffer
        pager.add_source(pypager.StringSource(""))  # page-buffer that gets replaced
        sync_file_to_pager()
        pager.run()

        quitting.set()
        update_thread.join(timeout=5)  # just to be sure a timeout
