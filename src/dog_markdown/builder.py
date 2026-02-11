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
        self._intermediate_stack = [[]]

    def add_heading(self, level: int, content: str | Paragraph) -> MarkdownBuilder:
        """Add a heading to the document.

        Args:
            level: Heading level (1-6)
            content: Heading text
        """
        self._intermediate_stack[-1].append(Heading(level=level, content=content))
        return self

    def add_paragraph(
        self, content: str | List[str | Text | Link | Image] | Paragraph
    ) -> MarkdownBuilder:
        """Add a paragraph to the document.

        Args:
            content: Paragraph content as string or list of elements
        """
        if isinstance(content, str):
            self._intermediate_stack[-1].append(
                Paragraph(children=[Text(content=content)])
            )
        elif isinstance(content, Paragraph):
            self._intermediate_stack[-1].append(content)
        else:
            children = []
            for item in content:
                if isinstance(item, str):
                    children.append(Text(content=item))
                else:
                    children.append(item)
            self._intermediate_stack[-1].append(Paragraph(children=children))
        return self

    def start_paragraph(self):
        self._intermediate_stack.append([])
        return self

    def end_paragraph(self):
        paragraph = Paragraph(children=self._intermediate_stack.pop())
        self._intermediate_stack[-1].append(paragraph)
        return self

    def paragraph(self):
        """Context manager for creating a paragraph.

        Usage:
            with builder.paragraph():
                builder.add_text("Hello ")
                builder.add_link("world", "https://example.com")
        """

        class ParagraphContext:
            def __init__(self, builder):
                self.builder = builder

            def __enter__(self):
                self.builder.start_paragraph()
                return self.builder

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    self.builder.end_paragraph()

        return ParagraphContext(self)

    def add_text(self, content: str, bold: bool = False) -> MarkdownBuilder:
        """Add plain text to the current element.

        Args:
            content: Text content
            bold: Whether to render text as bold (default: False)
        """
        self._intermediate_stack[-1].append(Text(content=content, bold=bold))
        return self

    def add_bold_text(self, content: str) -> MarkdownBuilder:
        """Add bold text to the current element.

        Args:
            content: Bold text content
        """
        return self.add_text(content, bold=True)

    def add_link(
        self, text: str, url: str, title: str | None = None
    ) -> MarkdownBuilder:
        """Add a link as a standalone paragraph.

        Args:
            text: Link display text
            url: Target URL
            title: Optional tooltip title
        """
        self._intermediate_stack[-1].append(Link(text=text, url=url, title=title))
        return self

    def add_image(
        self, alt: str, url: str, title: str | None = None
    ) -> MarkdownBuilder:
        """Add an image to the document.

        Args:
            alt: Alternative text for accessibility
            url: Image URL or path
            title: Optional tooltip title
        """
        # Images must be wrapped in a paragraph

        self._intermediate_stack[-1].append(Image(alt=alt, url=url, title=title))
        return self

    def add_code_block(
        self, content: str, language: str | None = None
    ) -> MarkdownBuilder:
        """Add a code block to the document.

        Args:
            content: Code content
            language: Optional programming language for syntax highlighting
        """
        self._intermediate_stack[-1].append(
            CodeBlock(content=content, language=language)
        )
        return self

    def add_blockquote(
        self,
        content: str
        | Document
        | List[
            str
            | Text
            | Link
            | Image
            | Paragraph
            | UnorderedList
            | CodeBlock
            | Blockquote
            | Table
        ],
    ) -> MarkdownBuilder:
        """Add a blockquote to the document.

        Args:
            content: Quote content as string, document, or list of elements
        """
        doc_children = []

        if isinstance(content, str):
            doc_children.append(Paragraph(children=[Text(content=content)]))
        elif isinstance(content, Document):
            doc_children.extend(content.children)
        else:
            for item in content:
                if isinstance(item, str):
                    doc_children.append(Paragraph(children=[Text(content=item)]))
                elif isinstance(item, Document):
                    doc_children.extend(item.children)
                else:
                    doc_children.append(item)

        self._intermediate_stack[-1].append(
            Blockquote(content=Document(children=doc_children))
        )
        return self

    def add_table(
        self,
        headers: List[str],
        rows: List[List[str | Text | Link | Image]],
        align: List[str | None] | None = None,
    ) -> MarkdownBuilder:
        """Add a table to the document.

        Args:
            headers: Table column headers
            rows: Table data rows
            align: Optional column alignment (left, center, right)
        """
        self._intermediate_stack[-1].append(
            Table(headers=headers, rows=rows, align=align)
        )  # type: ignore
        return self

    def start_unordered_list(self) -> MarkdownBuilder:
        """Start an unordered list.

        If already inside a list, this will create a nested list inside the current list item.
        """
        # If we're already inside a list, push current list to stack
        self._intermediate_stack.append([])

        return self


    def end_unordered_list(self) -> MarkdownBuilder:
        """End the current unordered list and add it to the document or parent list item."""
        # Create the list
        items = self._intermediate_stack.pop()

        list_items = []
        for x in items:
            if isinstance(x, Document):
                list_items.append(ListItem(content=x))
            elif isinstance(x, Paragraph) or isinstance(x, CodeBlock):
                list_items.append(ListItem(content=Document(children=[x])))
            else:
                raise Exception(f"unexpected item {x}")

        current_list = UnorderedList(items=list_items)
        self._intermediate_stack[-1].append(current_list)
        return self

    def unordered_list(self):
        """Context manager for creating an unordered list.

        Usage:
            with builder.unordered_list():
                builder.add_list_item("Item 1")
                builder.add_list_item("Item 2")
        """

        class UnorderedListContext:
            def __init__(self, builder):
                self.builder = builder

            def __enter__(self):
                self.builder.start_unordered_list()
                return self.builder

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    self.builder.end_unordered_list()

        return UnorderedListContext(self)

    def build(self) -> Document:
        """Build and return the final Document.

        Returns:
            Complete Markdown Document
        """
        return Document(children=self._intermediate_stack[-1].copy())

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
