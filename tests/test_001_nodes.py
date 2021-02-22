from core.importers import string_to_nodes
from core import cast_xml_property
from core.nodes.Node import BaseNode
from core.nodes.Node import Node


class TestBaseNode:
    def test_load_single_node(self):
        expected = BaseNode("a", {"name": "your_name"})
        assert string_to_nodes("<a name='your_name' />") == expected

    def test_nested_nodes(self):
        expected = BaseNode(
            "a", {"name": "a"}, children=[(BaseNode("b", {"name": "b"}))]
        )
        assert string_to_nodes("<a name='a'><b name='b'></b></a>") == expected

    def test_tag_props_conversion(self):
        assert cast_xml_property("age-int", "23") == ("age", 23)
        assert cast_xml_property("height-float", "1.87") == ("height", 1.87)
        assert cast_xml_property("data-json", '{"name": "mauro"}') == (
            "data",
            {"name": "mauro"},
        )


class TestNode:
    def test_empty_attributes(self):
        node = Node("any")
        assert node.attributes == {}

    def test_basic_attr(self):
        node = Node("any", attributes={"name": "mg", "age": 33})

        repr(node)
        assert node.attributes["name"] == "mg"
        assert node.name == "mg"

        kwargs = node.attributes.as_kwargs(sep=None)
        assert "age=33" in kwargs

        assert len(node.children(sep=None)) == 0
