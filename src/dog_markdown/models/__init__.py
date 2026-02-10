"""
dog-markdown: A type-safe Markdown generator for Python using Pydantic.

Design Decisions:
- Uses Pydantic models for type safety and validation
- ListItem accepts full Document objects for maximum flexibility in nested content
- Automatic space handling in Paragraph prevents awkward spacing between elements
- Multi-line content is merged into single paragraphs for clean output
- Nested elements are properly indented for valid Markdown structure
"""

from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class MarkdownElement(BaseModel):
    """Base class for all Markdown elements."""

    def to_str(self) -> str:
        """Convert element to Markdown string."""
        raise NotImplementedError(
            f"to_str() not implemented for {self.__class__.__name__}"
        )


class Text(MarkdownElement):
    """Plain text element."""

    content: str = Field(..., description="Plain text content")

    def to_str(self) -> str:
        lines = self.content.split("\n")
        lines = filter(lambda x: len(x) > 0, lines)
        content = " ".join(lines)
        return content


class Heading(MarkdownElement):
    """Heading element (H1-H6)."""

    level: int = Field(..., ge=1, le=6, description="Heading level (1-6)")
    content: str = Field(..., description="Heading content")

    def to_str(self) -> str:
        lines = self.content.split("\n")
        lines = filter(lambda x: len(x) > 0, lines)
        content = " ".join(lines)

        return f"{'#' * self.level} {content}"


class Paragraph(MarkdownElement):
    """Paragraph element containing multiple text elements."""

    children: List[Text | Link | Image] = Field(..., description="Paragraph content")

    def to_str(self) -> str:
        content_parts = []
        for child in self.children:
            part = child.to_str()
            if content_parts and not part.startswith(
                (" ", ".", ",", "!", "?", ":", ";", ")", "]", "}")
            ):
                last_char = content_parts[-1][-1] if content_parts[-1] else ""
                if not last_char.endswith((" ", "(", "[", "{", "<")):
                    content_parts.append(" ")
            content_parts.append(part)
        return "".join(content_parts)


class Link(MarkdownElement):
    """Hyperlink element."""

    text: str = Field(..., description="Link display text")
    url: str = Field(..., description="Target URL")
    title: str | None = Field(None, description="Link tooltip title")

    def to_str(self) -> str:
        if self.title:
            return f'[{self.text}]({self.url} "{self.title}")'
        return f"[{self.text}]({self.url})"


class Image(MarkdownElement):
    """Image element."""

    alt: str = Field(..., description="Alternative text for accessibility")
    url: str = Field(..., description="Image URL or path")
    title: str | None = Field(None, description="Image tooltip title")

    def to_str(self) -> str:
        if self.title:
            return f'![{self.alt}]({self.url} "{self.title}")'
        return f"![{self.alt}]({self.url})"


class ListItem(MarkdownElement):
    """Single list item."""

    content: Document = Field(..., description="List item content")

    def to_str(self) -> str:
        content_str = self.content.to_str().strip()
        lines = content_str.split("\n")
        lines = map(lambda x: "  " + x if x != "" else x, lines)
        content_str = "\n".join(lines)
        if not content_str.strip().startswith("-"):
            content_str = "- " + content_str.lstrip()
        return content_str


class UnorderedList(MarkdownElement):
    """Unordered (bullet) list."""

    items: List[ListItem] = Field(..., description="List items")

    def to_str(self) -> str:
        items_str = "\n\n".join(item.to_str() for item in self.items)
        return items_str.strip()


class CodeBlock(MarkdownElement):
    """Code block element with optional syntax highlighting."""

    content: str = Field(..., description="Code content")
    language: str | None = Field(
        None, description="Programming language for syntax highlighting"
    )

    def to_str(self) -> str:
        if self.language:
            return "```" + self.language + "\n" + self.content + "\n```"
        return "```\n" + self.content + "\n```"


class Blockquote(MarkdownElement):
    """Blockquote element for quoted text."""

    content: Document = Field(..., description="Quote content")

    def to_str(self) -> str:
        content_str = self.content.to_str()
        lines = content_str.split("\n")
        quoted_lines = [f"> {line}" if line.strip() else ">" for line in lines]
        return "\n".join(quoted_lines)


class Table(MarkdownElement):
    """Table element with rows and columns."""

    headers: List[str] = Field(..., description="Table column headers")
    rows: List[List[str | Text | Link | Image]] = Field(..., description="Table rows")
    align: List[str | None] | None = Field(
        None, description="Column alignment (left, center, right)"
    )

    def to_str(self) -> str:
        # Create header row
        header_row = f"| {' | '.join(self.headers)} |"

        # Create separator row
        if self.align:
            separator_cols = []
            for a in self.align:
                if a == "center":
                    separator_cols.append(":---:")
                elif a == "right":
                    separator_cols.append("---:")
                else:  # left or None
                    separator_cols.append("---")
        else:
            separator_cols = ["---"] * len(self.headers)
        separator_row = f"| {' | '.join(separator_cols)} |"

        # Create data rows
        data_rows = []
        for row in self.rows:
            cells = []
            for cell in row:
                if isinstance(cell, (Text, Link, Image)):
                    cells.append(cell.to_str())
                else:
                    cells.append(str(cell))
            data_rows.append(f"| {' | '.join(cells)} |")

        return "\n".join([header_row, separator_row] + data_rows)


class Document(MarkdownElement):
    """Top-level Markdown document."""

    children: List[
        Heading | Paragraph | UnorderedList | CodeBlock | Blockquote | Table
    ] = Field(..., description="Document content")

    def to_str(self) -> str:
        return "\n\n".join(child.to_str() for child in self.children)
