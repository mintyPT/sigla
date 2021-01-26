from xml.etree import ElementTree as ET

from sigla.classes.ImportNode import ImportNode


def load_xml_from_file(filename):
    return ET.parse(filename).getroot()


def load_string(str):
    return ET.fromstring(str).getroot()


def load_xml_string_into_nodes(s) -> ImportNode:
    obj: ET = ET.fromstring(s)
    node = process_xml(obj)
    return node


def process_xml(obj) -> ImportNode:
    node = ImportNode(obj.tag, attributes=obj.attrib.copy(), children=[])
    for child in obj:
        node.children.append(process_xml(child))
    return node
