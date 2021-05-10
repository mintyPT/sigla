from abc import ABC, abstractmethod

from sigla.data.Data import Data


class NodeABC(ABC):
    data: Data = None

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def finish(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.process()
