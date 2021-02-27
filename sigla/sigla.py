from pathlib import Path
from xml.etree import ElementTree
from sigla.core.cls.Data import Data
from sigla.core.nodes.NodeEcho import NodeEcho
from sigla.core.nodes.NodeFile import NodeFile
from sigla.core.nodes.NodeRoot import NodeRoot
from sigla.core.nodes.NodeTemplate import NodeTemplate
from sigla.types import NodeType
from sigla.utils import cast_property


def node_factory(tag, attributes) -> NodeType:
    if tag == "root":
        return NodeRoot(tag, attributes=attributes)
    elif tag == "file":
        return NodeFile(tag, attributes=attributes)
    elif tag == "echo":
        return NodeEcho(tag, attributes=attributes)
    else:
        return NodeTemplate(tag, attributes=attributes)


def data_to_node(node: Data, *, factory=node_factory) -> NodeType:
    """Takes Data classes and converts them to Node"""
    ret = factory(node.tag, node.attributes)

    for r in node.children:
        child = data_to_node(r, factory=factory)
        ret.append(child)

    return ret


def xml_to_data(obj) -> Data:
    attributes = obj.attrib.copy()
    new_attributes = {}

    for prop_name, prop_value in attributes.items():
        prop_name, prop_value = cast_property(prop_name, prop_value)
        new_attributes[prop_name] = prop_value

    node = Data(obj.tag, attributes=new_attributes, children=[])

    for child in obj:
        node.children.append(xml_to_data(child))

    return node


def string_to_data(s) -> Data:
    obj: ElementTree = ElementTree.fromstring(s)
    node = xml_to_data(obj)
    return node


def from_xml_string(source, *, factory=node_factory) -> NodeType:
    return data_to_node(string_to_data(source), factory=factory)


def from_xml_file(source, *, factory=node_factory) -> NodeType:
    source = Path(source).read_text()
    return from_xml_string(source, factory=factory)
