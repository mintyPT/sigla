from pathlib import Path


class FileTemplateLoader:
    def __init__(self, base_path, ext="jinja2"):
        self.base_path = base_path
        self.ext = ext

    def load(self, tag, bundle=None):
        path = Path(self.base_path)
        if bundle:
            path = path.joinpath(bundle)
        path = path.joinpath(f"{tag}.{self.ext}")
        return path
