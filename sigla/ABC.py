from abc import ABC, abstractmethod
from sigla.data.Data import Data


class NodeABC(ABC):
    data: Data = None

    @abstractmethod
    def process(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.process()


class PublicNodeABC(ABC):
    @abstractmethod
    def finish(self):
        pass


class TemplateEngineABC(ABC):
    @abstractmethod
    def render(self, template: str, filters: dict, **kwargs: any) -> str:
        pass


class TemplateLoaderABC(ABC):
    @abstractmethod
    def load(self, tag, bundle=None) -> str:
        pass