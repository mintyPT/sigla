from typing import Any, List

from sigla.data.data import Data


def flatten(lst: Any) -> List:
    """
    Recursively flattens a list
    """
    ret = []
    for item in lst:
        if type(item) == Data:
            ret.append(item)

        for child in item:
            if type(child) == list:
                ret += flatten(child)
            else:
                ret.append(child)
    return ret


def get_template_path(data: Data, extension: str = "jinja2") -> str:
    if bundle := data.get("bundle"):
        result = f"{bundle}/{data.tag}.{extension}"
    else:
        result = f"{data.tag}.{extension}"
    return result
