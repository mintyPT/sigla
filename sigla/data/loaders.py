from abc import ABC, abstractmethod
from xml.etree import ElementTree
from sigla.utils.type_casters import cast_dict
from sigla.data.data import Data


class DataLoader(ABC):
    @abstractmethod
    def load(self) -> Data:
        pass


class ElementTreeDataLoader(DataLoader):
    def __init__(self, element):
        self.element = element

    def load(self) -> Data:
        element = self.element
        children = element
        raw_attributes = element.attrib.copy()

        attributes = cast_dict(raw_attributes)
        children = [ElementTreeDataLoader(child).load() for child in children]

        return Data(
            tag=element.tag,
            attributes=attributes,
            children=children
        )


class XMLStringDataLoader(DataLoader):
    def __init__(self, source: str):
        self.source = source

    def load(self) -> Data:
        obj: ElementTree = ElementTree.fromstring(self.source)
        return ElementTreeDataLoader(obj).load()
