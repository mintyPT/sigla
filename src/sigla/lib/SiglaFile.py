import os

from sigla.lib.helpers.files import ensure_parent_dir


class SiglaFile:
    def __init__(self, content, path):
        self.content = content
        self.path = path

    def save(self, save_path):
        path = os.path.join(os.getcwd(), save_path, self.path)

        ensure_parent_dir(path)

        with open(path, "w") as h:
            h.write(self.content)
