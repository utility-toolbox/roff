# -*- coding=utf-8 -*-
r"""

"""
import markdown_it.rules_inline


__all__ = ['markdown_plugin_command']


def markdown_plugin_command(md: markdown_it.MarkdownIt) -> None:
    md.inline.ruler.before('backticks', 'command', _markdown_plugin_command)


def _markdown_plugin_command(state: markdown_it.rules_inline.StateInline, silent: bool) -> bool:
    pos = state.pos

    if state.src[pos] != "$":
        return False
    pos += 1
    if state.src[pos] != "`":
        return False

    start = pos
    pos += 1
    maximum = state.posMax

    # scan marker length
    while pos < maximum and (state.src[pos] == "`"):
        pos += 1

    marker = state.src[start:pos]
    opener_length = len(marker)

    if state.backticksScanned and state.backticks.get(opener_length, 0) <= start:
        if not silent:
            state.pending += marker
        state.pos += opener_length
        return True

    match_end = pos

    # Nothing found in the cache, scan until the end of the line (or until marker is found)
    while True:
        try:
            match_start = state.src.index("`", match_end)
        except ValueError:
            break
        match_end = match_start + 1

        # scan marker length
        while match_end < maximum and (state.src[match_end] == "`"):
            match_end += 1

        closer_length = match_end - match_start

        if closer_length == opener_length:
            # Found matching closer length.
            if not silent:
                token = state.push("command_inline", "code", 0)
                token.markup = marker
                token.content = state.src[pos:match_start].replace("\n", " ")
                if (
                    token.content.startswith(" ")
                    and token.content.endswith(" ")
                    and len(token.content.strip()) > 0
                ):
                    token.content = token.content[1:-1]
            state.pos = match_end
            return True

        # Some different length found, put it in cache as upper limit of where closer can be found
        state.backticks[closer_length] = match_start

    # Scanned through the end, didn't find anything
    state.backticksScanned = True

    if not silent:
        state.pending += marker
    state.pos += opener_length
    return True
