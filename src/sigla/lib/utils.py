from pathlib import Path
from xml.etree import ElementTree as ET


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def load_xml(filename):
    return ET.parse(filename).getroot()


def cast_array(v):
    if type(v) == list:
        return v
    return [v]