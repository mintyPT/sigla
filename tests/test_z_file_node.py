from sigla.core.nodes.NodeFile import NodeFile


class TestFileNode:
    def test_empty_attributes(self):
        node = NodeFile("any")

        try:
            node()
        except Exception:
            return
        assert (
            False
        ), "Should throw an exception since no `to` attr was provided"
