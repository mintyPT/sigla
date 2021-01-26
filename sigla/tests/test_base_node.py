from sigla.classes.nodes.BaseNode import BaseNode


class TestConvertToInternalClasses:
    def test_empty_attributes(self):
        node = BaseNode("any")
        assert node.attributes == {}
