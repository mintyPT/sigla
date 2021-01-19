from textwrap import dedent
from frontmatter import u, detect_format, handlers
from yaml.parser import ParserError


class FrontMatterHelper:
    @classmethod
    def split(cls, text, encoding="utf-8", handler=None):
        text = u(text, encoding).strip()

        # this will only run if a handler hasn't been set higher up
        handler = handler or detect_format(text, handlers)
        if handler is None:
            return None, text, None

        try:
            fm, content = handler.split(text)
        except ValueError:
            return None, text, handler

        return fm, content, handler

    @classmethod
    def parse(cls, fm, handler, metadata=None):
        if metadata is None:
            metadata = {}

        try:
            fm = handler.load(fm)
        except ParserError as e:
            print(
                dedent(
                    f"""
            ===
            There is an error on the following yaml (front matter)

            {fm}

            ===

            """
                )
            )
            raise e

        if isinstance(fm, dict):
            metadata.update(fm)

        return metadata
