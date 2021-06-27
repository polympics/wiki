"""Compile all files in IN_DIR to OUT_DIR, and add a JSON index."""
import json
import os
import pathlib
from typing import Any

from .config import INDEX_FILE, IN_DIR, OUT_DIR
from .content_file import ContentFile
from .renderer import compile


def compile_file(in_path: pathlib.Path) -> dict[str, Any]:
    """Compile a single file and return its metadata."""
    file = ContentFile(in_path.relative_to(IN_DIR))
    file.read_input()
    if in_path.suffix == '.md':
        compile(file)
    file.write_output()
    return file.options


def compile_all():
    """Compile all files in IN_DIR to OUT_DIR, and add a JSON index."""
    all_file_metadata = []
    for base_dir, _sub_dirs, files in os.walk(IN_DIR):
        for file in files:
            in_path = pathlib.Path(base_dir) / file
            file_metadata = compile_file(in_path)
            all_file_metadata.append(file_metadata)
    metadata = {'files': all_file_metadata}
    with open(OUT_DIR / INDEX_FILE, 'w') as index_file:
        json.dump(metadata, index_file, indent=4)


if __name__ == '__main__':
    compile_all()
