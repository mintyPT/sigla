import frontmatter
from xml.etree import ElementTree as ET


def load_xml(filename):
    return ET.parse(filename).getroot()


def load_string(str):
    return ET.fromstring(str).getroot()


def load_template(filepath):
    with open(filepath, "r") as h:
        metadata, template = frontmatter.parse(h.read())
        return template, metadata
