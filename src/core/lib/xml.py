import json
from xml.etree import ElementTree as ET


def load_xml_from_file(filename):
    return ET.parse(filename).getroot()


def cast_xml_property(prop_name, prop_value):
    if prop_name.endswith("-int"):
        return prop_name.replace("-int", ""), int(prop_value)
    elif prop_name.endswith("-float"):
        new_key = prop_name.replace("-float", "")
        new_value = float(prop_value)
    elif prop_name.endswith("-json"):
        new_key = prop_name.replace("-json", "")
        new_value = json.loads(prop_value)
    else:
        new_key = prop_name
        new_value = prop_value
    return new_key, new_value
