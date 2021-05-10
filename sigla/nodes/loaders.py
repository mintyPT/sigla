from sigla.data.Data import Data
from sigla.nodes.TagToNode import TagToNode
from sigla.nodes.NodeABC import NodeABC
from sigla.data.loaders import data_from_xml_string

node_factory = TagToNode()


def node_from_data(data: Data, *, factory=None) -> NodeABC:
    """Takes Data classes and converts them to Node"""
    if not factory:
        factory = TagToNode()

    ret = factory(data.tag, data.attributes)

    for r in data.children:
        child = node_from_data(r, factory=factory)
        ret.append(child)

    return ret


def node_from_xml_string(source: str, *, factory=None) -> NodeABC:
    data = data_from_xml_string(source)
    return node_from_data(data, factory=factory)


def load_node(kind, content, *, factory=None) -> NodeABC:
    if kind == "data":
        return node_from_data(content, factory=factory)
    elif kind == "xml_string":
        return node_from_xml_string(content, factory=factory)
