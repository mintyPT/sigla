from abc import ABC, abstractmethod

from sigla.data.data import Data


class AbstractNode(ABC):
    data: Data = None

    # Steps are
    # 1. Load X into Node/Data/Attributes
    # 2. Process
    # 3. Finish

    def __call__(self, *args, **kwargs):
        return self.process()

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def finish(self):
        pass
