"""Implementations of the @ directives."""
from .content_file import ContentFile


def set_title(file: ContentFile, *title_parts: str):
    """Set the title of a document."""
    file.options['title'] = ' '.join(title_parts)


def add_to_navbar(file: ContentFile):
    """Make a document linked to from the navbar."""
    file.options['navbar'] = True


DIRECTIVES = {
    'title': set_title,
    'navbar': add_to_navbar
}
