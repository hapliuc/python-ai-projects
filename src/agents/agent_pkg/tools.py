import os


def create_folder(path: str) -> str:
    os.popen(f"mkdir {path}")
    return f"Created directory {path}"


def create_file(path: str) -> str:
    os.popen(f"touch {path}")
    return f"Created file {path}"
