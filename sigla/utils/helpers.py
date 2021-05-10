import importlib
import types
from contextlib import suppress
from pathlib import Path


def ensure_dirs(*paths: str):
    """Ensure the paths exist"""
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def load_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


def load_filters_from(module_path):
    filters = {}
    with suppress(FileNotFoundError):
        filters_module = load_module("filters", module_path)
        if "FILTERS" in dir(filters_module):
            filters = filters_module.FILTERS
    return filters


# import importlib
# import importlib.machinery
# from typing import Type, TypeVar

# T = TypeVar("T")

# def import_reference(ref: str) -> Type[T]:
#     """Imports stuff from modules dynamically"""
#     p, m = ref.rsplit(".", 1)
#     mod = importlib.import_module(p)
#     res: Type[T] = getattr(mod, m)
#     return res
