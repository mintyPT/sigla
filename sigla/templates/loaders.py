from abc import ABC, abstractmethod
from pathlib import Path


class TemplateLoaderABC(ABC):
    @abstractmethod
    def get_path(self, tag, *, bundle=None) -> str:
        pass


class FileTemplateLoader(TemplateLoaderABC):
    def __init__(self, base_path, ext="jinja2"):
        self.base_path = base_path
        self.ext = ext

    def get_path(self, tag, *, bundle=None) -> str:
        path = Path(self.base_path)
        if bundle:
            path = path.joinpath(bundle)
        path = path.joinpath(f"{tag}.{self.ext}")
        return path
