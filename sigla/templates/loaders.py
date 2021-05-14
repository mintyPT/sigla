from abc import abstractmethod, ABC
from pathlib import Path


class TemplateLoaderAbc(ABC):
    @abstractmethod
    def load(self, tag, bundle=None) -> str:
        pass


class FileTemplateLoader(TemplateLoaderAbc):
    def __init__(self, base_path, ext="jinja2"):
        self.base_path = base_path
        self.ext = ext

    def load(self, tag, bundle=None) -> str:
        path = Path(self.base_path)
        if bundle:
            path = path.joinpath(bundle)
        path = path.joinpath(f"{tag}.{self.ext}")
        return path
