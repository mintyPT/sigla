from pathlib import Path


def ensure_dirs(*paths: str):
    for path_ in paths:
        Path(path_).mkdir(parents=True, exist_ok=True)
