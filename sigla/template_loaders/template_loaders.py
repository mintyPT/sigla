from abc import ABC, abstractmethod
from pathlib import Path

from sigla.template_loaders.exceptions import TemplateDoesNotExistError


class TemplateLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        """
        This should load the "raw" template
        """
        pass

    @abstractmethod
    def write(self, content: str, path: str) -> None:
        """
        This should load the "raw" template
        """
        pass


class FileTemplateLoader(TemplateLoader):
    path: Path

    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self, path: str) -> str:
        path = self.path.joinpath(path)
        if not path.exists():
            raise TemplateDoesNotExistError(path)
        return path.read_text()

    def write(self, content: str, path: str) -> None:
        if path in ["buffer.jinja2"]:
            raise Exception("should not happend")
        self.path.joinpath(path).parent.mkdir(parents=True, exist_ok=True)
        self.path.joinpath(path).write_text(content)
