from pathlib import Path


def ensure_dirs(*paths):
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)


def ensure_parent_dir(*paths):
    for path_ in paths:
        Path(path_).parent.mkdir(parents=True, exist_ok=True)
