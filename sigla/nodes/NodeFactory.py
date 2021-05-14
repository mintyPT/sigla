from sigla.nodes.NodeEcho import NodeEcho
from sigla.nodes.NodeFile import NodeFile
from sigla.nodes.NodeRoot import NodeRoot
from sigla.nodes.NodeTemplate import NodeTemplate
from sigla.templates.engines import JinjaEngine
from sigla import config
from sigla.templates.loaders import FileTemplateLoader


class NodeFactory:
    default = NodeTemplate
    reference = {
        "root": NodeRoot,
        "file": NodeFile,
        "echo": NodeEcho,
    }

    def __init__(self):
        self.engine = JinjaEngine()
        self.loader = FileTemplateLoader(config.path.templates, "jinja2")

    def __call__(self, tag: str, attributes: object):
        node_creator = self.reference.get(tag)
        default_creator = self.default

        if node_creator:
            return node_creator(tag, self.engine, self.loader, attributes=attributes)
        else:
            return default_creator(tag, self.engine, self.loader, attributes=attributes)
