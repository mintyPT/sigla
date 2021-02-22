from pathlib import Path
from core.errors import TemplateDoesNotExistError
from core.nodes.NodeTemplate import NodeTemplate


class AutoNodeTemplate(NodeTemplate):
    base_path = "tests/templates/%s.jinja2"

    def load_test_template(self, name):
        return Path(self.base_path % name).read_text()

    def raw_template_loader(self, tag) -> str:
        try:
            return self.load_test_template(tag)
        except FileNotFoundError:
            raise TemplateDoesNotExistError(tag, self)
