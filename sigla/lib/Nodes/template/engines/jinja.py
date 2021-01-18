import pydash as _
from jinja2 import Environment, FileSystemLoader


def as_kwargs_filter(obj):
    kwargs = []
    for k, v in obj.items():
        if type(v) == int:
            kwargs.append(f"{k}={v}")
        else:
            kwargs.append(f'{k}="{v}"')
    return ", ".join(kwargs)


def map_get_filter(arr, key):
    return [_.get(o, key) for o in arr]


def without_filter(obj, *args):
    result = {}
    for k, v in obj.items():
        if k not in args:
            result[k] = v
    return result


def jinja(template: str, filters=None, **kwargs):
    if filters is None:
        filters = {}

    env = Environment()

    env.filters["without"] = without_filter
    env.filters["as_kwargs"] = as_kwargs_filter
    env.filters["map_get"] = map_get_filter

    env.filters["get_nested"] = lambda arr, field: map(
        lambda el: _.get(el, field), arr
    )

    env.filters["flatten"] = _.flatten
    env.filters["flatten_depth"] = _.flatten_depth
    env.filters["flatten_deep"] = _.flatten_deep
    env.filters["get"] = _.get
    env.filters["map"] = _.map_
    env.filters["filter"] = _.filter_
    env.filters["uniq"] = _.uniq

    for k, v in filters.items():
        env.filters[k] = v

    template = env.from_string(template)

    return template.render(**kwargs)