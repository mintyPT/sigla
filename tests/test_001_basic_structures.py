from sigla.utils import cast_xml_property, import_node
from sigla.sigla import string_to_data
from sigla.core.cls.Data import Data

Node = import_node()


class TestBaseNode:
    def test_load_single_node(self):
        expected = Data("a", {"name": "your_name"})
        assert string_to_data("<a name='your_name' />") == expected

    def test_nested_nodes(self):
        expected = Data(
            "a", {"name": "a"}, children=[(Data("b", {"name": "b"}))]
        )
        assert string_to_data("<a name='a'><b name='b'></b></a>") == expected

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
