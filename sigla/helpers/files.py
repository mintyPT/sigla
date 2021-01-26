from pathlib import Path


def ensure_dirs(*paths):
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def ensure_parent_dir(*paths):
    for path_ in paths:
        ensure_dirs(Path(path_).parent)


def ensure_file(filepath, content=""):
    if Path(filepath).exists():
        return
    with open(filepath, "w") as h:
        h.write(content)
