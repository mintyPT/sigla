from contextlib import suppress

from sigla.core.nodes.NodeFile import NodeFile


class TestFileNode:
    def test_empty_attributes(self):
        node = NodeFile("any")

        with suppress(AttributeError):
            node()
            assert (
                False
            ), "Should throw an exception since no `to` attr was provided"
