from abc import ABC, abstractmethod


class TemplateEngineABC(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        pass


class TemplateLoaderABC(ABC):
    @abstractmethod
    def load(self, tag, *, bundle=None) -> str:
        pass