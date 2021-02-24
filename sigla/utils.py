import json
import types
import importlib
import importlib.machinery
from contextlib import suppress
from pathlib import Path
from textwrap import dedent
from typing import TypeVar

from frontmatter import u, detect_format, handlers
from yaml.parser import ParserError

#
from sigla import config


def ensure_dirs(*paths: str):
    """Ensure the paths exist"""
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def import_reference(ref: str) -> type:
    """Imports stuff from modules dinamically"""
    p, m = ref.rsplit(".", 1)
    mod = importlib.import_module(p)
    res = getattr(mod, m)
    return res


def import_node_list() -> type:
    """Imports NodeList"""
    ref = config.cls.node_list
    res = import_reference(ref)
    return res


def import_node() -> type:
    """Imports NodeList"""
    ref = config.cls.node
    res = import_reference(ref)
    return res


def cast_xml_property(prop_name, prop_value):
    if prop_name.endswith("-int"):
        return prop_name.replace("-int", ""), int(prop_value)
    elif prop_name.endswith("-float"):
        new_key = prop_name.replace("-float", "")
        new_value = float(prop_value)
    elif prop_name.endswith("-json"):
        new_key = prop_name.replace("-json", "")
        new_value = json.loads(prop_value)
    elif prop_name.endswith("-bool"):
        new_key = prop_name.replace("-bool", "")
        new_value = True if prop_value in ["True", "true", "1"] else False
    else:
        new_key = prop_name
        new_value = prop_value
    return new_key, new_value


def load_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


def load_filters_from(module_path):
    filters = {}
    module_name = "filters"
    with suppress(FileNotFoundError):
        filters_module = load_module(module_name, module_path)
        if "FILTERS" in dir(filters_module):
            filters = filters_module.FILTERS
    return filters


def frontmatter_split(text, *, encoding="utf-8", handler=None):
    text = u(text, encoding).strip()

    # this will only run if a handler hasn't been set higher up
    handler = handler or detect_format(text, handlers)
    if handler is None:
        return None, text, None

    try:
        fm, content = handler.split(text)
    except ValueError:
        return None, text, handler

    return fm, content, handler


def frontmatter_parse(fm, handler, *, metadata=None):
    if metadata is None:
        metadata = {}

    try:
        fm = handler.load(fm)
    except ParserError as e:
        print(
            dedent(
                f"""
        ===
        There is an error on the following yaml (front matter)

        {fm}

        ===

        """
            )
        )
        raise e

    if isinstance(fm, dict):
        metadata.update(fm)

    return metadata
