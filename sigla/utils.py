import json
import types
import warnings
import importlib
import importlib.machinery
from contextlib import suppress
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Type, TypeVar

from frontmatter import u, detect_format, handlers
from yaml.parser import ParserError

#
from sigla import config

if TYPE_CHECKING:
    from sigla.core.cls.Node import Node
    from sigla.core.cls.NodeList import NodeList


def ensure_dirs(*paths: str):
    """Ensure the paths exist"""
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


T = TypeVar("T")


def import_reference(ref: str) -> Type[T]:
    """Imports stuff from modules dynamically"""
    p, m = ref.rsplit(".", 1)
    mod = importlib.import_module(p)
    res: Type[T] = getattr(mod, m)
    return res


def import_node_list() -> Type["NodeList"]:
    """Imports NodeList"""
    ref = config.cls.node_list
    res = import_reference(ref)
    return res


def import_node() -> Type["Node"]:
    """Imports NodeList"""
    ref = config.cls.node
    res = import_reference(ref)
    return res


def cast_property(prop_name, prop_value):
    if prop_name.endswith("-int"):
        return prop_name.replace("-int", ""), int(prop_value)

    elif prop_name.endswith("-float"):
        new_key = prop_name.replace("-float", "")
        new_value = float(prop_value)
        return new_key, new_value

    elif prop_name.endswith("-json"):
        new_key = prop_name.replace("-json", "")
        new_value = json.loads(prop_value)
        return new_key, new_value

    elif prop_name.endswith("-bool"):
        new_key = prop_name.replace("-bool", "")
        new_value = True if prop_value in ["True", "true", "1"] else False
        return new_key, new_value

    new_key = prop_name
    new_value = prop_value
    return new_key, new_value


def cast_xml_property(prop_name, prop_value):
    warnings.warn("This will be deprecated. Please us `cast_property`")
    return cast_property(prop_name, prop_value)


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


def get_template_path(base_path, tag, ext="jinja2", bundle=None):
    path = Path(base_path)
    if bundle:
        path = path.joinpath(bundle)
    path = path.joinpath(f"{tag}.{ext}")
    return path
