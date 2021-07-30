from copy import deepcopy
from typing import Optional
from xml.etree.ElementTree import XML, Element

from helpers.helpers import cast_dict, key_matching_filter, pipe, rename_key
from sigla.data.data import Data


def convert_xml_string_to_data(xml: str) -> Data:
    return pipe(
        xml,
        XML,
        _xml_element_to_data,
        _cast_data_attributes,
        _replace_ids_with_data,
    )


def _xml_element_to_data(obj: Element) -> Data:
    return Data(
        obj.tag,
        children=[_xml_element_to_data(child) for child in obj],
        **(cast_dict(obj.attrib.copy())),
    )


def _cast_data_attributes(data: Data) -> Data:
    data.own_attributes = cast_dict(data.own_attributes)

    for child in data:
        _cast_data_attributes(child)

    return data


def _replace_ids_with_data(data: Data, root: Optional[Data] = None) -> Data:
    if root is None:
        root = data

    rename_all_keys_ending_with_id(data, root)

    for child in data:
        _replace_ids_with_data(child, root=root)

    return data


def rename_all_keys_ending_with_id(data: Data, root: Optional[Data] = None) -> None:
    def endswith_id(string: str) -> bool:
        return string.endswith("-id")

    _attributes_temp = deepcopy(data.own_attributes)
    for key, value in key_matching_filter(_attributes_temp, endswith_id):
        found_element = root.find_by_id(value) if root else None
        value_ = found_element.duplicate(parent=data) if found_element else None
        rename_key(
            data.own_attributes,
            key_old=key,
            key=key.replace("-id", ""),
            value=value_,
        )
