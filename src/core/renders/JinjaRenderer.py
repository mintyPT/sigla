from jinja2 import Environment, BaseLoader

from core.renders.AbstractRenderer import AbstractRenderer


class JinjaRenderer(AbstractRenderer):
    def render(self, tpl: str, filters: dict, **kwargs: any) -> str:
        env = Environment(loader=BaseLoader)
        env.filters.update(filters)
        template = env.from_string(tpl)
        return template.render(**kwargs)
