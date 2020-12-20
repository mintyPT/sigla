import pydash as _
from jinja2 import FileSystemLoader, Environment


def as_kwargs_filter(obj):
    kwargs = []
    for k, v in obj.items():
        if type(v) == int:
            kwargs.append(f'{k}={v}')
        else:
            kwargs.append(f'{k}="{v}"')
    return ', '.join(kwargs)


def map_get_filter(arr, key):
    return [_.get(o, key) for o in arr]


def without_filter(obj, *args):
    result = {}
    for k, v in obj.items():
        if k not in args:
            result[k] = v
    return result


def render_njk(template_full_path, **kwargs):
    with open(template_full_path, 'r') as h:
        file_loader = FileSystemLoader('.')
        env = Environment(loader=file_loader)
        env.filters['without'] = without_filter
        env.filters['as_kwargs'] = as_kwargs_filter
        env.filters['map_get'] = map_get_filter

        env.filters['get_nested'] = lambda arr, field: map(lambda el: _.get(el, field), arr)

        env.filters['flatten'] = _.flatten

        # template = Template(h.read())
        template = env.get_template(template_full_path)

        return template.render(**kwargs)
