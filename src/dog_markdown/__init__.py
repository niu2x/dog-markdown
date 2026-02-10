"""
dog-markdown: A type-safe Markdown generator for Python using Pydantic.

This is the main entry point for the library. Import models directly or use the builder API.
"""

# Export all models
from .models import (
    Document,
    Heading,
    Paragraph,
    Text,
    Link,
    Image,
    UnorderedList,
    ListItem,
    CodeBlock,
    Blockquote,
    Table,
)

# Export builder API
from .builder import MarkdownBuilder, markdown

__all__ = [
    "Document",
    "Heading",
    "Paragraph",
    "Text",
    "Link",
    "Image",
    "UnorderedList",
    "ListItem",
    "CodeBlock",
    "Blockquote",
    "Table",
    "MarkdownBuilder",
    "markdown",
]

__version__ = "1.0.0"
