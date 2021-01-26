from textwrap import dedent

from sigla.lib.helpers.ImportNode import ImportNode
from sigla.lib.importers.xml import load_xml


class TestXMLLoading:
    def test_one_element(self):
        node = ImportNode("a", {"name": "myname"}, [])
        source = dedent("""<a name="myname" />""")
        assert load_xml(source) == node

    def test_two_elements(self):
        nodes = ImportNode(
            "a", {"name": "a"}, [(ImportNode("b", {"name": "b"}, []))]
        )
        input = "<a name='a'><b name='b'></b></a>"
        assert load_xml(input) == nodes
