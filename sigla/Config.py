import environ


@environ.config(prefix="")
class Config:
    @environ.config
    class Paths:
        root_directory = environ.var(".sigla")
        templates_folder = environ.var("templates")
        snapshots_folder = environ.var("snapshots")
        definitions_folder = environ.var("definitions")
        scripts_folder = environ.var("scripts")

        filters_filename = environ.var("filters.py")

        @property
        def templates(self):
            return f"{self.root_directory}/{self.templates_folder}"

        @property
        def scripts(self):
            return f"{self.root_directory}/{self.scripts_folder}"

        @property
        def snapshots(self):
            return f"{self.root_directory}/{self.snapshots_folder}"

        @property
        def definitions(self):
            return f"{self.root_directory}/{self.definitions_folder}"

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
