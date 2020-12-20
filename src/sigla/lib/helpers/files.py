from pathlib import Path


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
