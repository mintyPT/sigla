from abc import abstractmethod, ABC

from sigla.data.data import Data
from sigla.node_factory import NodeFactory
from sigla.nodes import NodeABC
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


def load_node(kind, content, *, factory=None) -> NodeABC:
    if kind == "data":
        loader = DataToNodeLoader(content, factory)
    elif kind == "xml_string":
        loader = XMLToNodeLoader(content, factory)
    else:
        raise NotImplementedError(f"No loader implemented for {kind}")

    return loader.load()
