from textwrap import dedent

from frontmatter import u, detect_format, handlers
from yaml.parser import ParserError


class FrontMatter:
    def __init__(self, handler=None):
        self.handler = handler

    def split(self, raw_content, *, encoding="utf-8"):
        raw_content = u(raw_content, encoding).strip()

        # this will only run if a handler hasn't been set higher up
        self.handler = self.handler or detect_format(raw_content, handlers)
        if self.handler is None:
            return None, raw_content, None

        try:
            fm, content = self.handler.split(raw_content)
        except ValueError:
            return None, raw_content, self.handler

        return fm, content, self.handler

    def parse(self, raw_frontmatter, *, metadata=None):
        if metadata is None:
            metadata = {}

        try:
            raw_frontmatter = self.handler.load(raw_frontmatter)
        except ParserError as e:
            print(
                dedent(
                    f"""
            ===
            There is an error on the following yaml (front matter)

            {raw_frontmatter}

            ===

            """
                )
            )
            raise e

        if isinstance(raw_frontmatter, dict):
            metadata.update(raw_frontmatter)

        return metadata
