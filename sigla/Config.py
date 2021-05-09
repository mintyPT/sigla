import environ


@environ.config(prefix="")
class Config:
    @environ.config
    class Paths:
        root_directory = environ.var(".sigla")
        templates_filename = environ.var("templates")
        snapshots_filename = environ.var("snapshots")
        definitions_filename = environ.var("definitions")
        filters_filename = environ.var("filters.py")

        @property
        def templates(self):
            return f"{self.root_directory}/{self.templates_filename}"

        @property
        def snapshots(self):
            return f"{self.root_directory}/{self.snapshots_filename}"

        @property
        def definitions(self):
            return f"{self.root_directory}/{self.definitions_filename}"

        @property
        def filters(self):
            return f"{self.root_directory}/{self.filters_filename}"

    @environ.config
    class Cls:
        node_list = environ.var("sigla.core.node_lists.NodeList")
        node = environ.var("sigla.core.nodes.Node")

    path: Paths = environ.group(Paths)
    cls: Cls = environ.group(Cls)


config = environ.to_config(Config)
