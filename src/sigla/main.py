from sigla import process_node
from sigla.lib.helpers.loaders import load_xml, load_string


def run(file=None, content=None):
    if file:
        root = load_xml(file)
    elif content:
        root = load_string(content)
    else:
        raise Exception("You need to prove a file or some content")

    process_node(root)
