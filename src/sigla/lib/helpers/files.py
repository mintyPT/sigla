from pathlib import Path


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
