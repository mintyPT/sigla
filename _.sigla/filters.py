"""
Export filters to use on the templates using the `FILTERS` variable
"""
import json

from sigla import register_filter


@register_filter("dump")
def dump(var):
    return json.dumps(var, indent=4)
