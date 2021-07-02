from abc import ABC, abstractmethod

from sigla.data.data import Data
from sigla.templates import TemplateEngineABC, TemplateLoaderABC


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
