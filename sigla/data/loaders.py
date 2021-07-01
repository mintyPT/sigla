from abc import ABC, abstractmethod
from xml.etree import ElementTree
from sigla.utils.type_casters import cast_property
from sigla.data.data import Data


class DataLoader(ABC):
    @abstractmethod
    def load(self) -> Data:
        pass


class ElementTreeDataLoader(DataLoader):
    def __init__(self, element):
        self.element = element

    def load(self) -> Data:
        attributes = self.element.attrib.copy()
        new_attributes = {}

        for prop_name, prop_value in attributes.items():
            prop_name, prop_value = cast_property(prop_name, prop_value)
            new_attributes[prop_name] = prop_value

        data = Data(tag=self.element.tag, attributes=new_attributes, children=[])

        for child in self.element:
            child_data = ElementTreeDataLoader(child).load()
            data.children.append(child_data)

        return data


class XMLStringDataLoader(DataLoader):
    def __init__(self, source: str):
        self.source = source

    def load(self) -> Data:
        obj: ElementTree = ElementTree.fromstring(self.source)
        return ElementTreeDataLoader(obj).load()

