from __future__ import annotations
from typing import List, Union, Optional
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
        # lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: len(x) > 0, lines)
        content = " ".join(lines)
        return content


class Heading(MarkdownElement):
    """Heading element (H1-H6)."""

    level: int = Field(..., ge=1, le=6, description="Heading level (1-6)")
    content: str = Field(..., description="Heading content")

    def to_str(self) -> str:

        lines = self.content.split("\n")
        # lines = map(lambda x: x.strip(), lines)
        lines = filter(lambda x: len(x) > 0, lines)
        content = " ".join(lines)

        return f"{'#' * self.level} {content}"


class Paragraph(MarkdownElement):
    """Paragraph element containing multiple text elements."""

    children: List[Text | Link] = Field(..., description="Paragraph content")

    def to_str(self) -> str:
        return f"{''.join(child.to_str() for child in self.children)}"


class Link(MarkdownElement):
    """Hyperlink element."""

    text: str = Field(..., description="Link display text")
    url: str = Field(..., description="Target URL")
    title: str | None = Field(None, description="Link tooltip title")

    def to_str(self) -> str:
        if self.title:
            return f'[{self.text}]({self.url} "{self.title}")'
        return f"[{self.text}]({self.url})"


class ListItem(MarkdownElement):
    """Single list item."""

    content: Document = Field(..., description="List item content")

    def to_str(self) -> str:
        content_str = self.content.to_str().strip()

        lines = content_str.split("\n")
        lines = map(lambda x: "  " + x if x != "" else x, lines)
        content_str = "\n".join(lines)
        if not content_str.strip().startswith("- "):
            content_str = "- " + content_str[2:]
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
    language: Optional[str] = Field(
        None, description="Programming language for syntax highlighting"
    )

    def to_str(self) -> str:
        if self.language:
            return "```" + self.language + "\n" + self.content + "\n```"
        return "```\n" + self.content + "\n```"


class Document(MarkdownElement):
    """Top-level Markdown document."""

    children: List[Union[Heading, Paragraph, UnorderedList, CodeBlock]] = Field(
        ..., description="Document content"
    )

    def to_str(self) -> str:
        return "\n\n".join(child.to_str() for child in self.children)
