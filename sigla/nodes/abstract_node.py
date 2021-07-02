from abc import ABC, abstractmethod

from sigla.data.data import Data


class AbstractNode(ABC):
    data: Data = None

    @abstractmethod
    def process(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.process()
