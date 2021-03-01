from jinja2 import Environment, BaseLoader

__RENDERS = dict()


def register(f):
    __RENDERS[f.__name__] = f
    return f


def render(plugin, template, **kw):
    return __RENDERS[plugin](template, **kw)


@register
def jinja(template: str, filters: dict, **kwargs: any) -> str:
    env = Environment(loader=BaseLoader())
    env.filters.update(filters)
    template = env.from_string(template)
    return template.render(**kwargs)
