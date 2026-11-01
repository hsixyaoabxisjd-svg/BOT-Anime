from pathlib import Path


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def list_files(directory: str):
    return [str(p) for p in Path(directory).iterdir()]
