from typing import Union

from sigla.helpers.files import ensure_parent_dir, write


class FileOutput:
    path: str = None
    content: str = None

    def __init__(self, path, content):
        self.path = path
        self.content = content

    def save(self):
        ensure_parent_dir(self.path)
        write(self.path, self.content)

    def __eq__(self, o: Union[object, "FileOutput"]) -> bool:
        if type(self) != type(o):
            return False
        if self.content != o.content:
            return False
        if self.path != o.path:
            return False
        return True
