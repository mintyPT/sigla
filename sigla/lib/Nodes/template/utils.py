import textwrap

import frontmatter
from frontmatter import u
from yaml.parser import ParserError


def fm_split(text, encoding="utf-8", handler=None):
    text = u(text, encoding).strip()

    # this will only run if a handler hasn't been set higher up
    handler = handler or frontmatter.detect_format(text, frontmatter.handlers)
    if handler is None:
        return None, text, None

    try:
        fm, content = handler.split(text)
    except ValueError:
        return None, text, handler

    return fm, content, handler


def fm_parse_fm(fm, handler, metadata=None):
    if metadata is None:
        metadata = {}

    try:
        fm = handler.load(fm)
    except ParserError as e:
        print("")
        print(
            textwrap.dedent(
                f"""
                ===
                There should be an error on the following yaml (front matter)

                {fm}

                ===

                """
            )
        )
        raise e

    if isinstance(fm, dict):
        metadata.update(fm)

    return metadata
