import os


def create_folder(path: str) -> str:
    os.popen(f"mkdir {path}")
    return f"Created directory {path}"


def create_file(name: str) -> str:
    os.popen(f"touch {name}")
    return f"Created file {name}"
