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


def remove_consecutive_blank_lines(text, max_consecutive=2):
    """
    删除文本中连续的空白行，最多保留指定数量的空白行

    参数:
        text (str): 输入文本
        max_consecutive (int): 最多保留的连续空白行数，默认为2

    返回:
        str: 处理后的文本
    """
    lines = text.splitlines()
    result_lines = []
    consecutive_blank_count = 0

    for line in lines:
        # 检查当前行是否为空行（strip后为空）
        is_blank = line.strip() == ""

        if not is_blank:
            # 非空行直接保留，并重置空白行计数器
            result_lines.append(line)
            consecutive_blank_count = 0
        else:
            # 空行处理
            consecutive_blank_count += 1

            if consecutive_blank_count <= max_consecutive:
                # 保留空白行，但不超过最大限制
                result_lines.append("")
            # 否则跳过这个空白行

    # 将处理后的行重新组合成文本
    result = "\n".join(result_lines)

    # 可选：去除开头和结尾的空白行
    result = result.strip("\n")

    return result


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


class Heading(MarkdownElement):
    """Heading element (H1-H6)."""

    level: int = Field(..., ge=1, le=9, description="Heading level (1-9)")
    content: str | Paragraph = Field(..., description="Heading content")

    def to_str(self) -> str:
        if isinstance(self.content, Paragraph):
            content = self.content.to_str()
        else:
            lines = self.content.split("\n")
            lines = filter(lambda x: len(x) > 0, lines)
            content = " ".join(lines)

        return f"{'#' * self.level} {content}"


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
    indent: int = 1

    def to_str(self) -> str:
        items_str = "\n\n".join(
            item.to_str() for item in self.items
        )

        lines = items_str.split("\n")
        lines = map(lambda x: "  " * (self.indent - 1) + x, lines)
        items_str = "\n".join(lines)
        return remove_consecutive_blank_lines(items_str)


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
        return remove_consecutive_blank_lines(
            "\n\n".join(child.to_str() for child in self.children)
        )
