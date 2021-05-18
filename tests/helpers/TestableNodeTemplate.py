from sigla.nodes.NodeTemplate import NodeTemplate


class TestableNodeTemplate(NodeTemplate):
    create_template = False

    def finish(self):
        pass

    @staticmethod
    def get_filters():
        return {"wrap": lambda e: f"[{e}]"}
