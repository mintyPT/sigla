from abc import ABC, abstractmethod


class AbstractPublicNode(ABC):
    @abstractmethod
    def finish(self):
        pass