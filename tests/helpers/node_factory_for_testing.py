from sigla.nodes.TagToNode import TagToNode
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader
from tests.helpers.AutoNodeTemplate import AutoNodeTemplate


class TestingNodeFromTag(TagToNode):
    default = AutoNodeTemplate

    def __init__(self):
        super().__init__()
        self.loader = FileTemplateLoader("tests/templates/", "jinja2")



node_factory_for_testing = TestingNodeFromTag()
