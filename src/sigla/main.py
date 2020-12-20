import logging

from sigla import process_node
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.helpers.loaders import load_xml, load_string


def run(file=None, content=None):
    if file:
        root = load_xml(file)
    elif content:
        root = load_string(content)
    else:
        raise Exception("You need to prove a file or some content")

    result = process_node(root)
    for r in result:
        if type(r) == SiglaFile:
            logging.info(f"[Render] Saving generated file to {r.path}")
            r.save()
        elif type(r) == str:
            print(r)
        else:
            raise NotImplementedError(f"No final handling implemented for {type(r)}")