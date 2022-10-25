from abc import ABC, abstractmethod
from typing import Any

from jinja2 import Environment, BaseLoader, Template


class TemplateEngineABC(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: Any) -> str:
        pass


class JinjaEngine(TemplateEngineABC):
    def render(self, template: str, filters: dict, **kwargs: Any) -> str:
        env = Environment(loader=BaseLoader())
        env.filters.update(filters)
        jinja_tpl: Template = env.from_string(template)
        return jinja_tpl.render(**kwargs)
