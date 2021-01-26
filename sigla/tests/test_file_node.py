from sigla.classes.nodes.FileNode import FileNode


class TestConvertToInternalClasses:
    def test_empty_attributes(self):
        node = FileNode("any")

        try:
            node.process()
        except Exception:
            return
        assert False, "Should throw an exception"
