from sigla import config

from sigla.nodes.node_echo import NodeEcho
from sigla.nodes.node_file import NodeFile
from sigla.nodes.node_root import NodeRoot
from sigla.nodes.node_template import NodeTemplate

from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader
from sigla.templates import TemplateEngineABC, TemplateLoaderABC


class NodeFactory:
    default = NodeTemplate
    reference = {
        "root": NodeRoot,
        "file": NodeFile,
        "echo": NodeEcho,
    }

    def __init__(
        self,
        engine: TemplateEngineABC = None,
        loader: TemplateLoaderABC = None,
    ):
        if engine is None:
            engine = JinjaEngine()

        if loader is None:
            loader = FileTemplateLoader(config.path.templates, "jinja2")

        self.engine = engine
        self.loader = loader

    def __call__(self, tag: str, attributes: object):
        node_creator = self.reference.get(tag)

        if node_creator:
            return node_creator(
                tag, self.engine, self.loader, attributes=attributes
            )
        else:
            return self.default(
                tag, self.engine, self.loader, attributes=attributes
            )
