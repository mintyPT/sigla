from abc import ABC, abstractmethod
from jinja2 import Environment, BaseLoader


class TemplateEngineABC(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        pass


class JinjaEngine(TemplateEngineABC):
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        env = Environment(loader=BaseLoader())
        env.filters.update(filters)
        template = env.from_string(template)
        return template.render(**kwargs)
