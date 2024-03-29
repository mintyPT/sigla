from sigla.node_factory import NodeFactory
from sigla.templates.loaders import FileTemplateLoader
from tests.helpers.TestableNodeTemplate import TestableNodeTemplate


class TestableNodeFactory(NodeFactory):
    default = TestableNodeTemplate

    def __init__(self):
        super().__init__()
        self.loader = FileTemplateLoader("tests/templates/", "jinja2")


node_factory_for_testing = TestableNodeFactory()
