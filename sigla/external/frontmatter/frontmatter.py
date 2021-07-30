from textwrap import dedent
from typing import Any, Callable, Dict, Optional, Tuple

from frontmatter import detect_format, handlers, u
from yaml.parser import ParserError


def parse_with_handler(
    handler: Callable, raw_frontmatter: str, *, metadata: Dict = None
) -> Dict[str, Any]:
    return parse(raw_frontmatter, metadata=metadata, handler=handler)


def parse_with_transformation(
    template: str, transformer: Callable, *args: Any
):
    variables, _, handler = split(template)
    if not variables or not handler:
        return {}
    variables = transformer(*args, variables)
    return parse_with_handler(handler, variables)


def split(
    raw_content: str,
    *,
    encoding: str = "utf-8",
    handler: Optional[Callable] = None,
) -> Tuple[Dict, str, Callable]:
    raw_content = u(raw_content, encoding)

    # this will only run if a handler hasn't been set higher up
    handler = handler or detect_format(raw_content, handlers)
    if handler is None:
        return None, raw_content, None

    try:
        fm, content = handler.split(raw_content)
    except ValueError:
        return None, raw_content, handler

    return fm, content, handler


def get_content(template: str) -> str:
    frontmatter, content, handler = split(template)
    return content


def parse(
    raw_frontmatter: str, *, metadata=None, handler=None
) -> Dict[str, Any]:
    metadata = {} if metadata is None else metadata

    try:
        frontmatter = handler.load(raw_frontmatter)
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

    if isinstance(frontmatter, dict):
        metadata.update(frontmatter)

    return metadata
