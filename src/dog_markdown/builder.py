"""
Builder API for procedural Markdown document creation.
Provides a fluent interface for building documents without directly creating models.
"""

from __future__ import annotations
from typing import List
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


class MarkdownBuilder:
    """Fluent builder for creating Markdown documents procedurally."""

    def __init__(self):
        self._children = []
        self._current_list_items = []

    def add_heading(self, level: int, content: str) -> "MarkdownBuilder":
        """Add a heading to the document.

        Args:
            level: Heading level (1-6)
            content: Heading text
        """
        self._children.append(Heading(level=level, content=content))
        return self

    def add_paragraph(
        self, content: str | List[str | Text | Link | Image]
    ) -> "MarkdownBuilder":
        """Add a paragraph to the document.

        Args:
            content: Paragraph content as string or list of elements
        """
        if isinstance(content, str):
            self._children.append(Paragraph(children=[Text(content=content)]))
        else:
            children = []
            for item in content:
                if isinstance(item, str):
                    children.append(Text(content=item))
                else:
                    children.append(item)
            self._children.append(Paragraph(children=children))
        return self

    def add_text(self, content: str) -> "MarkdownBuilder":
        """Add a plain text paragraph to the document.

        Args:
            content: Text content
        """
        return self.add_paragraph(content)

    def add_link(
        self, text: str, url: str, title: str | None = None
    ) -> "MarkdownBuilder":
        """Add a link as a standalone paragraph.

        Args:
            text: Link display text
            url: Target URL
            title: Optional tooltip title
        """
        return self.add_paragraph([Link(text=text, url=url, title=title)])

    def add_image(
        self, alt: str, url: str, title: str | None = None
    ) -> "MarkdownBuilder":
        """Add an image to the document.

        Args:
            alt: Alternative text for accessibility
            url: Image URL or path
            title: Optional tooltip title
        """
        # Images must be wrapped in a paragraph
        self._children.append(
            Paragraph(children=[Image(alt=alt, url=url, title=title)])
        )
        return self

    def add_code_block(
        self, content: str, language: str | None = None
    ) -> "MarkdownBuilder":
        """Add a code block to the document.

        Args:
            content: Code content
            language: Optional programming language for syntax highlighting
        """
        self._children.append(CodeBlock(content=content, language=language))
        return self

    def add_blockquote(
        self, content: str | List[str | Text | Link | Image | Paragraph]
    ) -> "MarkdownBuilder":
        """Add a blockquote to the document.

        Args:
            content: Quote content as string or list of elements
        """
        if isinstance(content, str):
            content = [content]

        doc_children = []
        for item in content:
            if isinstance(item, str):
                doc_children.append(Paragraph(children=[Text(content=item)]))
            else:
                doc_children.append(item)
        self._children.append(Blockquote(content=Document(children=doc_children)))
        return self

    def add_table(
        self,
        headers: List[str],
        rows: List[List[str | Text | Link | Image]],
        align: List[str | None] | None = None,
    ) -> "MarkdownBuilder":
        """Add a table to the document.

        Args:
            headers: Table column headers
            rows: Table data rows
            align: Optional column alignment (left, center, right)
        """
        self._children.append(Table(headers=headers, rows=rows, align=align))  # type: ignore
        return self

    def start_list(self) -> "MarkdownBuilder":
        """Start an unordered list."""
        self._current_list_items = []
        return self

    def add_list_item(
        self, content: str | List[str | Text | Link | Image | Paragraph]
    ) -> "MarkdownBuilder":
        """Add an item to the current list.

        Args:
            content: List item content
        """
        if isinstance(content, str):
            doc = Document(children=[Paragraph(children=[Text(content=content)])])
        else:
            # If it's a list of elements, wrap them in a single paragraph
            paragraph_children = []
            for item in content:
                if isinstance(item, str):
                    paragraph_children.append(Text(content=item))
                elif isinstance(item, Paragraph):
                    # If it's already a paragraph, add its children directly
                    paragraph_children.extend(item.children)
                else:
                    paragraph_children.append(item)
            doc = Document(children=[Paragraph(children=paragraph_children)])
        self._current_list_items.append(ListItem(content=doc))
        return self

    def end_list(self) -> "MarkdownBuilder":
        """End the current list and add it to the document."""
        if self._current_list_items:
            self._children.append(UnorderedList(items=self._current_list_items))
            self._current_list_items = []
        return self

    def build(self) -> Document:
        """Build and return the final Document.

        Returns:
            Complete Markdown Document
        """
        return Document(children=self._children.copy())

    def to_str(self) -> str:
        """Build and convert the document to Markdown string.

        Returns:
            Markdown string representation
        """
        return self.build().to_str()


def markdown() -> MarkdownBuilder:
    """Create a new MarkdownBuilder instance.

    Returns:
        New MarkdownBuilder
    """
    return MarkdownBuilder()
