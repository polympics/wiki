"""Extension to commonmark.py that adds @ directives."""
import re

import commonmark.blocks
from commonmark.blocks import Block, BlockStarts, Parser
from commonmark.node import Node
from commonmark.render.html import HtmlRenderer

from .content_file import ContentFile
from .directives import DIRECTIVES


SYMBOL = '@'
QUOTE_MARK = '"'
ESCAPE = '\\'
SEPARATOR = ' '

BLOCK_NAME = 'cms_directive'


class CmsDirective(Block):
    """The block-level node composed of a directive."""

    accepts_lines = False

    @staticmethod
    def continue_(parser: Parser, container: Node) -> int:
        """Tell the parser not to continue to the next line."""
        return 1

    @staticmethod
    def finalize(parser: Parser, block: Node):
        """Make sure the content is not parsed as inline markdown."""
        block.literal = block.string_content
        block.string_content = None

    @staticmethod
    def can_contain(t: str) -> bool:
        """Don't let this node contain any other."""
        return False


def block_starts_cms_directive(
        block_starts: BlockStarts, parser: Parser, container: Node) -> int:
    """Check if a line is an @ directive."""
    if parser.indented:
        return 0
    if not parser.current_line[parser.next_nonspace:].startswith(SYMBOL):
        return 0
    parser.close_unmatched_blocks()
    container = parser.add_child(BLOCK_NAME, parser.next_nonspace)
    container.string_content = parser.current_line[parser.offset + 1:]
    parser.advance_offset(
        len(parser.current_line) - parser.offset, False)
    return 2


def render_cms_directive(renderer: HtmlRenderer, node: Node, entering: bool):
    """Render the directive as an empty line."""
    renderer.cr()
    renderer.cms_directives.append(node.literal)


# Inject everything.
BlockStarts.cms_directive = block_starts_cms_directive
commonmark.blocks.reMaybeSpecial = re.compile(
    r'^[#`~*+_=<>0-9-' + SYMBOL + ']')
BlockStarts.METHODS.insert(0, BLOCK_NAME)
Parser.blocks[BLOCK_NAME] = CmsDirective
HtmlRenderer.cms_directive = render_cms_directive


def parse_args(raw_args: str) -> list[str]:
    """Parse raw arguments for a directive in to a list of arguments."""
    if not raw_args.startswith(QUOTE_MARK):
        raw_args = SEPARATOR + raw_args
    args = []
    in_escape = in_string = False
    for char in raw_args:
        if in_escape:
            args[-1] += char
            in_escape = False
        elif char == ESCAPE:
            in_escape = True
        elif in_string:
            if char == QUOTE_MARK:
                in_string = False
            else:
                args[-1] += char
        else:
            if char == QUOTE_MARK:
                in_string = True
            elif char == SEPARATOR:
                args.append('')
            else:
                args[-1] += char
    if in_string:
        raise ValueError('Reached EOL while parsing string.')
    if in_escape:
        raise ValueError('Reached EOL while parsing escape sequence.')
    return args


def parse_directive(file: ContentFile, raw: str):
    """Parse a directive and modify the file in-place."""
    parts = raw.split(SEPARATOR, maxsplit=1)
    directive = parts[0].lower()
    if directive not in DIRECTIVES:
        raise ValueError(f'Unknown directive "{directive}".')
    if len(parts) == 1:
        args = []
    else:
        args = parse_args(parts[1])
    DIRECTIVES[directive](file, *args)


def compile(file: ContentFile):
    """Compile a source file to HTML and directives."""
    parser = Parser()
    ast = parser.parse(file.content)
    renderer = HtmlRenderer()
    renderer.cms_directives = []
    file.content = renderer.render(ast)
    for directive in renderer.cms_directives:
        parse_directive(file, directive)
