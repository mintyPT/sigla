from sigla.nodes.TagToNode import TagToNode
from tests.helpers.AutoNodeTemplate import AutoNodeTemplate


class TestingNodeFromTag(TagToNode):
    default = AutoNodeTemplate


node_factory_for_testing = TestingNodeFromTag()
