from copy import deepcopy
from xml.etree.ElementTree import XML, Element

from sigla.data.data import Data
from sigla.helpers import cast_dict, iter_with_filter


def element_to_data(obj: Element) -> Data:
    return Data(
        obj.tag,
        children=[element_to_data(child) for child in obj],
        **(cast_dict(obj.attrib.copy()))
    )


def cast_attributes(data: Data) -> Data:
    data.own_attributes = cast_dict(data.own_attributes)

    for child in data:
        cast_attributes(child)

    return data


def key_endswith_id(key: str, value: any) -> bool:
    return key.endswith("-id")


def replace_ids_with_references(data: Data, root: Data = None) -> Data:
    if root is None:
        root = data

    _attributes_temp = deepcopy(data.own_attributes)
    for key, value in iter_with_filter(_attributes_temp, key_endswith_id):
        rename_dict_attribute(
            data.own_attributes,
            key=key,
            new_key=key.replace("-id", ""),
            new_value=root.find_by_id(value),
        )

    for child in data:
        replace_ids_with_references(child, root=root)

    return data


# TODO move this
def rename_dict_attribute(dict_, key, new_key, new_value):
    dict_[new_key] = new_value
    del dict_[key]
    return dict_


# TODO move this
def pipe(first, *args):
    for fn in args:
        first = fn(first)
    return first


def load_data_from_element_tree(obj: Element) -> Data:
    return pipe(
        obj,
        element_to_data,
        cast_attributes,
        replace_ids_with_references,
    )


def convert_xml_string_to_data(xml: str) -> Data:
    return load_data_from_element_tree(XML(xml))
