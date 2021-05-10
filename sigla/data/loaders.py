from xml.etree import ElementTree
from sigla.utils.type_casters import cast_property
from sigla.data.Data import Data


def data_from_element_tree(element):
    attributes = element.attrib.copy()
    new_attributes = {}

    for prop_name, prop_value in attributes.items():
        prop_name, prop_value = cast_property(prop_name, prop_value)
        new_attributes[prop_name] = prop_value

    data = Data(tag=element.tag, attributes=new_attributes, children=[])

    for child in element:
        child_data = data_from_element_tree(child)
        data.children.append(child_data)

    return data


def data_from_xml_string(source: str) -> Data:
    obj: ElementTree = ElementTree.fromstring(source)
    return data_from_element_tree(obj)
