from sigla.sigla import string_to_data, data_to_node
from sigla.core.outputs.OutputEcho import OutputEcho
from sigla.core.outputs.OutputFile import OutputFile
from .helpers.node_factory_for_testing import node_factory_for_testing


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
        got = data_to_node(
            string_to_data(provided), factory=node_factory_for_testing
        )()
        expected = [
            OutputFile(path="result.txt", content="core"),
            OutputEcho(content="core"),
        ]

        assert got == expected
