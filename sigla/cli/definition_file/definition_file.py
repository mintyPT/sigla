from pathlib import Path


class DefinitionFile:
    def __init__(self, name: str) -> None:
        self.name = name
        self.filepath = Path(name)

    def exists(self) -> bool:
        return self.filepath.exists()

    def write(self, content: str) -> None:
        self.filepath.write_text(content)

    def read(self) -> str:
        return self.filepath.read_text()
