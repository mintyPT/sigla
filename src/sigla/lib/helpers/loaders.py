from xml.etree import ElementTree as ET


def load_xml(filename):
    return ET.parse(filename).getroot()


def load_string(str):
    return ET.fromstring(str).getroot()
