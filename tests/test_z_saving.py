from core.importers import base_node_to_node, string_to_nodes
from .helpers.node_factory_for_testing import node_factory_for_testing
from core.outputs.OutputEcho import OutputEcho
from core.outputs.OutputFile import OutputFile


class TestOutputs:
    def test_fm_child(self):
        provided = """
            <root>
                <file to="result.txt">
                    <print_name name="core"/>
                </file>
                <echo>
                    <print_name name="core"/>
                </echo>
            </root>
        """
        got = base_node_to_node(
            string_to_nodes(provided), factory=node_factory_for_testing
        )()
        expected = [
            OutputFile(path="result.txt", content="core"),
            OutputEcho(content="core"),
        ]

        assert got == expected
