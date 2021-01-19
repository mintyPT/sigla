from xml.etree import ElementTree as ET

from sigla.lib2.helpers.ImportNode import ImportNode
from sigla.lib2.funcs import from_import_node_to_base_node


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
    return from_import_node_to_base_node(load_xml(source))