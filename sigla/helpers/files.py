from pathlib import Path


def ensure_dirs(*paths):
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def ensure_parent_dir(*paths):
    for path_ in paths:
        ensure_dirs(Path(path_).parent)


def ensure_file(filepath, content=""):
    if exists(filepath):
        return
    write(filepath, content)


def exists(filepath):  # pragma: no cover
    return Path(filepath).exists()


def write(p, content):  # pragma: no cover
    with open(p, "w") as h:
        h.write(content)


def read(p):  # pragma: no cover
    with open(p, "r") as h:
        return h.read()
