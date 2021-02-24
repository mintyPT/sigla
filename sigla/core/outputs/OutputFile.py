from pathlib import Path
from typing import Union

from sigla.utils import ensure_dirs


class OutputFile:
    path: str = None
    content: str = None

    def __init__(self, path, content):
        self.path = path
        self.content = content

    def save(self):
        ensure_dirs(Path(self.path).parent)
        with open(self.path, "w") as h:
            h.write(self.content)

    def __eq__(self, o: Union[object, "OutputFile"]) -> bool:
        if type(self) != type(o):
            return False
        if self.content != o.content:
            return False
        if self.path != o.path:
            return False
        return True

    def __repr__(self):
        return f"[file-output: {self.content}]"
