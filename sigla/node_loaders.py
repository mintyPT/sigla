from abc import abstractmethod, ABC
from sigla.data.loaders import XMLStringDataLoader


class NodeLoader(ABC):
    @abstractmethod
    def load(self):
        pass


class DataToNodeLoader(NodeLoader):
    def __init__(self, data, factory):
        self.data = data
        self.factory = factory

    def load(self):
        ret = self.factory(self.data.tag, self.data.attributes)

        for r in self.data.children:
            loader = DataToNodeLoader(r, self.factory)
            child = loader.load()
            ret.append(child)

        return ret


class XMLToNodeLoader(DataToNodeLoader):
    def __init__(self, data, factory):
        data = XMLStringDataLoader(data).load()
        super().__init__(data, factory)
