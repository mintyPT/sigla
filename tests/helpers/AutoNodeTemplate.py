from pathlib import Path

from sigla.errors import TemplateDoesNotExistError
from sigla.core.nodes.NodeTemplate import NodeTemplate


class AutoNodeTemplate(NodeTemplate):
    base_path = "tests/templates/"

    def load_test_template(self, name):
        return Path(self.get_template_path(name)).read_text()

    def raw_template_loader(self, tag) -> str:
        try:
            return self.load_test_template(tag)
        except FileNotFoundError:
            raise TemplateDoesNotExistError(tag, self)

    @staticmethod
    def get_filters():
        return {"wrap": lambda e: f"[{e}]"}
