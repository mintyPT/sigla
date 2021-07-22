from pathlib import Path

from sigla.template_loaders.errors import TemplateDoesNotExistError
from sigla.template_loaders.template_loader import TemplateLoader


class FileTemplateLoader(TemplateLoader):
    def __init__(self, path):
        self.path = Path(path)

    @staticmethod
    def get_tag(bundle, tag, extension="jinja2"):
        if bundle:
            return f"{bundle}/{tag}.{extension}"
        else:
            return f"{tag}.{extension}"

    def load(self, tag, *, bundle=None):
        path = self.get_path_for_tag(tag, bundle=bundle)
        if not path.exists():
            raise TemplateDoesNotExistError(tag)
        return path.read_text()

    def write(self, content, tag, *, bundle=None):
        self.get_path_for_tag(tag, bundle=bundle).write_text(content)

    def get_path_for_tag(self, tag, *, bundle=None) -> Path:
        tag = self.get_tag(bundle, tag)
        return self.path.joinpath(tag)
