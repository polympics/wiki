"""Dataclass for a content file and parsing metadata."""
import dataclasses
import os
import pathlib
from typing import Any

from .config import IN_DIR, OUT_DIR


@dataclasses.dataclass
class ContentFile:
    """A content file and parsing metadata."""

    input_path: pathlib.Path
    content: str = None
    _options: dict[str, Any] = None

    @property
    def options(self) -> dict[str, Any]:
        """Get this file's metadata, initialising if needed."""
        if not self._options:
            title = self.input_path.stem.title().replace('_', ' ')
            self._options = {'title': title, 'navbar': False}
        return self._options

    @options.setter
    def options(self, new_options: dict[str, Any]):
        """Overwrite the file's metadata."""
        self._options = new_options

    def read_input(self):
        """Load the source of the document."""
        with open(self.input_path) as file:
            self.content = file.read()

    def write_output(self):
        """Write the content to the output path."""
        rel_path = str(self.input_path.relative_to(IN_DIR))
        out_path = OUT_DIR / rel_path
        out_dir = out_path.parent
        out_path = str(out_path)
        if out_path.lower().endswith('.md'):
            out_path = out_path[:-3] + '.html'
            rel_path = rel_path[:-3] + '.html'
        self.options['path'] = rel_path
        os.makedirs(out_dir, exist_ok=True)
        with open(out_path, 'w') as file:
            file.write(self.content)
