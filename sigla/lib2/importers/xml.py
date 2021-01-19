from xml.etree import ElementTree as ET

from sigla.lib2.ImportNode import ImportNode
from sigla.lib2.funcs import from_nodes_to_internal


def load_xml(s) -> ImportNode:
    obj: ET = ET.fromstring(s)
    node = process_xml(obj)
    return node


def process_xml(obj) -> ImportNode:
    node = ImportNode(obj.tag, attributes=obj.attrib.copy(), children=[])
    for child in obj:
        node.children.append(process_xml(child))
    return node


def import_from_xml_string(source):
    return from_nodes_to_internal(load_xml(source))