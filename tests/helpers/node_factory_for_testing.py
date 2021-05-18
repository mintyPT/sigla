from sigla.nodes.NodeFactory import NodeFactory
from sigla.templates.loaders import FileTemplateLoader
from tests.helpers.TestableNodeTemplate import TestableNodeTemplate


class TestingNodeFromTag(NodeFactory):
    default = TestableNodeTemplate

    def __init__(self):
        super().__init__()
        self.loader = FileTemplateLoader("tests/templates/", "jinja2")


node_factory_for_testing = TestingNodeFromTag()
