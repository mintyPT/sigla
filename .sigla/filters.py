"""
Export filters to use on the templates using the `FILTERS` variable
"""
import json
from sigla.filters import *


@register_filter("dump")
def dump(var):
    return json.dumps(var, indent=4)


@register_filter("wrap")
def wrap(e):
    return f"[{e}]"
