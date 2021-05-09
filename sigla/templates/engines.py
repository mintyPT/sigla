from abc import ABC, abstractmethod
from jinja2 import Environment, BaseLoader


class TemplateEngine(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        pass


class JinjaEngine(TemplateEngine):
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        env = Environment(loader=BaseLoader())
        env.filters.update(filters)
        template = env.from_string(template)
        return template.render(**kwargs)
