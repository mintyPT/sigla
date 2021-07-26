from typing import Optional

from jinja2 import BaseLoader, Environment


def render_template(
    template: str, filters: Optional[dict] = None, **kwargs
) -> str:
    env = Environment(loader=BaseLoader(), keep_trailing_newline=True)
    if filters:
        env.filters.update(filters)

    jinja_template = env.from_string(
        template, globals=None, template_class=None
    )
    result = jinja_template.render(**kwargs)

    return result
