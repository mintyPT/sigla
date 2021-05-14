from abc import ABC, abstractmethod
from jinja2 import Environment, BaseLoader


class TemplateEngineAbc(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        pass


class JinjaEngine(TemplateEngineAbc):
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        env = Environment(loader=BaseLoader())
        env.filters.update(filters)
        template = env.from_string(template)
        return template.render(**kwargs)
