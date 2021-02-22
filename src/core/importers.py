from xml.etree import ElementTree as ET

from core import node_factory
from core.nodes.Node import BaseNode, Node
from core import cast_xml_property


def base_node_to_node(node: BaseNode, factory=node_factory) -> Node:
    ret = factory(node.tag, node.attributes)

    for r in node.children:
        node_res = base_node_to_node(r, factory=factory)

        ret.append(node_res)

    return ret


def import_from_xml_string(source, factory=node_factory) -> Node:
    return base_node_to_node(string_to_nodes(source), factory=factory)


def string_to_nodes(s) -> BaseNode:
    obj: ET = ET.fromstring(s)
    node = xml_to_base_nodes(obj)
    return node


def xml_to_base_nodes(obj) -> BaseNode:
    attributes = obj.attrib.copy()
    new_attributes = {}

    for prop_name, prop_value in attributes.items():
        prop_name, prop_value = cast_xml_property(prop_name, prop_value)
        new_attributes[prop_name] = prop_value

    node = BaseNode(obj.tag, attributes=new_attributes, children=[])
    for child in obj:
        node.children.append(xml_to_base_nodes(child))
    return node
