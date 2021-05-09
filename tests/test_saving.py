import unittest

from sigla import load_node
from .helpers.node_factory_for_testing import node_factory_for_testing


class TestOutputs(unittest.TestCase):
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
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )()

        self.assertEqual(got[0].to, "result.txt")
        self.assertEqual(got[0].content, "core")
        self.assertEqual(got[1].content, "core")
