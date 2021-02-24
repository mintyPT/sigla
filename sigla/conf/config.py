import environ


@environ.config(prefix="")
class Config:
    @environ.config
    class Paths:
        templates = environ.var(".sigla/templates")
        snapshots = environ.var(".sigla/snapshots")
        definitions = environ.var(".sigla/definitions")
        filters = environ.var(".sigla/filters.py")

    @environ.config
    class Cls:
        node_list = environ.var("sigla.core.cls.NodeList.NodeList")
        node = environ.var("sigla.core.cls.Node.Node")

    path: Paths = environ.group(Paths)
    cls: Cls = environ.group(Cls)


config = environ.to_config(Config)
