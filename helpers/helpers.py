import importlib
import json
import types
from pathlib import Path
from typing import Callable


def key_matching_filter(dic: dict, validate_function: Callable):
    """
    Takes a dict and iterates over it as long as the key, value pair passes
    the test
    """
    for key, value in dic.items():
        if validate_function(key):
            yield key, value


value_casters = {
    "int": int,
    "float": float,
    "json": json.loads,
    "bool": lambda v: v.lower() in ["true", "1"],
}


def cast_property(name: str, value):
    kind = name.split("-")[-1]
    if caster := value_casters.get(kind):
        return name.replace(f"-{kind}", ""), caster(value)
    return name, value


def cast_dict(attributes: dict) -> dict:
    """
    Takes a dict of props and casts them if necessary
    """
    key_values = [
        cast_property(name, value) for name, value in attributes.items()
    ]

    return dict(key_values)


def ensure_dirs(*paths: str):
    """Ensure the paths exist"""
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def load_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


def join(lst_of_strings, separator="\n"):
    return separator.join(lst_of_strings)


def map_and_join(map_function, the_list, *, sep=""):
    return join(
        map(
            map_function,
            the_list,
        ),
        sep,
    )


def pipe(first, *args):
    for fn in args:
        first = fn(first)
    return first


def str_endswith_id(string_: str) -> bool:
    return string_.endswith("-id")


def rename_key(dict_, key_old, key, value=None):
    # assign old value if no value is provided
    value = value if value else dict_[key_old]

    dict_[key] = value
    del dict_[key_old]

    return dict_


def uniq(lst):
    """
    Given a list returns only the list of unique values
    """
    ret = []
    for item in lst:
        if item not in ret:
            ret.append(item)
    return ret
