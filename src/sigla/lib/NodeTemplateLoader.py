import os
from pathlib import Path

from sigla import Node
from sigla.lib.helpers.files import ensure_parent_dir
from sigla.lib.helpers.loaders import load_template


class NodeTemplateLoader:
    templates_directory = "./.sigla/templates"
    create_missing_templates = True

    def __init__(self, name):
        self.name = name
        self.path = Path(os.path.join(self.templates_directory, self.name))

    def ensure(self, default_value):
        """ Ensure the file really exists """

        if not self.create_missing_templates:
            return

        ensure_parent_dir(self.path)
        if self.path.exists():
            return
        with open(self.path, "w") as h:
            h.write(default_value)

    def load(self):
        return load_template(self.path)

    @classmethod
    def from_node(cls, node: Node):
        name = node.get_template_name()
        name = name.replace("-", "/")
        name = f"{name}.njk"

        return cls(name)