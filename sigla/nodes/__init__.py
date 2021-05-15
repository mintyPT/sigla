from abc import ABC, abstractmethod

from sigla.data.Data import Data
from sigla.templates import TemplateEngineABC, TemplateLoaderABC


class NodeABC(ABC):
    data: Data = None

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def __init__(
        self,
        tag: str,
        engine: TemplateEngineABC,
        template_loader: TemplateLoaderABC,
        *,
        attributes=None,
        children=None,
        parent_attributes=None
    ):
        pass

    def __call__(self, *args, **kwargs):
        return self.process()


class PublicNodeABC(ABC):
    @abstractmethod
    def finish(self):
        pass
