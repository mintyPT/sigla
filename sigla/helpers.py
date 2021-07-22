import json
from pathlib import Path
from typing import Callable


def iter_with_filter(dic, fun):
    for key, value in dic.items():
        if fun(key, value):
            yield key, value


casters = {
    "int": int,
    "float": float,
    "json": json.loads,
    "bool": lambda v: v.lower() in ["true", "1"],
}


def cast_property(name: str, value):
    kind = name.split("-")[-1]
    if caster := casters.get(kind):
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
