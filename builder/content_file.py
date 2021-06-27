"""Dataclass for a content file and parsing metadata."""
import dataclasses
import os
import pathlib
from typing import Any

from .config import IN_DIR, OUT_DIR


@dataclasses.dataclass
class ContentFile:
    """A content file and parsing metadata."""

    path: pathlib.Path
    content: bytes = None
    _options: dict[str, Any] = None

    @property
    def options(self) -> dict[str, Any]:
        """Get this file's metadata, initialising if needed."""
        if not self._options:
            title = self.path.stem.title().replace('_', ' ')
            self._options = {'title': title, 'navbar': False}
        return self._options

    @options.setter
    def options(self, new_options: dict[str, Any]):
        """Overwrite the file's metadata."""
        self._options = new_options

    def read_input(self):
        """Load the source of the document."""
        with open(IN_DIR / self.path, 'rb') as file:
            self.content = file.read()

    def write_output(self):
        """Write the content to the output path."""
        out_path = OUT_DIR / self.path
        self.options['path'] = str(self.path)
        os.makedirs(out_path.parent, exist_ok=True)
        with open(out_path, 'wb') as file:
            file.write(self.content)
