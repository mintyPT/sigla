from pathlib import Path
from sigla.ABC import TemplateLoaderABC


class FileTemplateLoader(TemplateLoaderABC):
    def __init__(self, base_path, ext="jinja2"):
        self.base_path = base_path
        self.ext = ext

    def load(self, tag, *, bundle=None) -> str:
        path = Path(self.base_path)
        if bundle:
            path = path.joinpath(bundle)
        path = path.joinpath(f"{tag}.{self.ext}")
        return path
