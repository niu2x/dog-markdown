#!/usr/bin/env python3
"""Test script to verify all code examples in README files work correctly."""

from dog_markdown import (
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
    MarkdownBuilder,
    markdown,
)


def test_core_models():
    """Test core model API examples."""
    print("Testing core models API...")

    # Document example
    doc = Document(
        children=[
            Heading(level=1, content="My Document"),
            Paragraph(children=[Text(content="Hello World!")]),
        ]
    )
    result = doc.to_str()
    assert "# My Document" in result
    assert "Hello World!" in result

    # Heading example
    heading = Heading(level=2, content="Section Title")
    assert heading.to_str() == "## Section Title"

    # Rich text heading
    heading = Heading(
        level=3,
        content=Paragraph(
            children=[
                Text(content="See our "),
                Link(text="API docs", url="/api"),
                Text(content=" for details"),
            ]
        ),
    )
    assert "### See our [API docs](/api) for details" in heading.to_str()

    # Paragraph example
    paragraph = Paragraph(
        children=[
            Text(content="Visit our "),
            Link(text="website", url="https://example.com"),
            Text(content=" or check out our "),
            Image(alt="Logo", url="/logo.png"),
        ]
    )
    result = paragraph.to_str()
    assert (
        "Visit our [website](https://example.com) or check out our ![Logo](/logo.png)"
        in result
    )

    # Text example
    text = Text(content="Plain text")
    assert text.to_str() == "Plain text"

    bold_text = Text(content="Important note", bold=True)
    assert bold_text.to_str() == "**Important note**"

    # Link example
    link = Link(text="Download", url="/file.pdf", title="Download PDF document")
    assert link.to_str() == '[Download](/file.pdf "Download PDF document")'

    # Image example
    image = Image(alt="Dog picture", url="/dog.jpg", title="A cute dog")
    assert image.to_str() == '![Dog picture](/dog.jpg "A cute dog")'

    # UnorderedList example
    list = UnorderedList(
        items=[
            ListItem(
                content=Document(
                    children=[Paragraph(children=[Text(content="Item 1")])]
                )
            ),
            ListItem(
                content=Document(
                    children=[Paragraph(children=[Text(content="Item 2")])]
                )
            ),
        ]
    )
    result = list.to_str()
    assert "- Item 1" in result
    assert "- Item 2" in result

    # CodeBlock example
    code_block = CodeBlock(
        content="def add(a, b):\n    return a + b", language="python"
    )
    assert "```python" in code_block.to_str()
    assert "def add(a, b):" in code_block.to_str()

    # Blockquote example
    quote = Blockquote(
        content=Document(
            children=[Paragraph(children=[Text(content="To be or not to be")])]
        )
    )
    assert "> To be or not to be" in quote.to_str()

    # Table example
    table = Table(
        headers=["Feature", "Status"],
        rows=[["Type safety", "✅"], ["Builder API", "✅"]],
        align=["left", "center"],
    )
    result = table.to_str()
    assert "| Feature | Status |" in result
    assert "| --- | :---: |" in result
    assert "| Type safety | ✅ |" in result

    print("✓ Core models API tests passed!")


def test_builder_api():
    """Test Builder API examples."""
    print("\nTesting Builder API...")

    # Basic usage
    builder = MarkdownBuilder()
    doc = (
        builder.add_heading(1, "My Document")
        .add_paragraph("Welcome to dog-markdown!")
        .add_code_block("print('Hello World')", language="python")
        .build()
    )

    result = doc.to_str()
    assert "# My Document" in result
    assert "Welcome to dog-markdown!" in result
    assert "```python" in result

    # Quick start
    doc = (
        markdown()
        .add_heading(2, "Quick Start")
        .add_paragraph("Easy to use builder API")
        .to_str()
    )

    assert "## Quick Start" in doc
    assert "Easy to use builder API" in doc

    # Rich text paragraph
    builder = MarkdownBuilder()
    with builder.paragraph():
        builder.add_bold_text("Note:")
        builder.add_text(" This is a ")
        builder.add_bold_text("very important")
        builder.add_text(" message with ")
        builder.add_link("links", "https://example.com")

    result = builder.to_str()
    assert (
        "**Note:** This is a **very important** message with [links](https://example.com)"
        in result
    )

    # List operations
    builder = MarkdownBuilder()
    with builder.unordered_list():
        builder.add_paragraph("Simple list item")

        with builder.paragraph():
            builder.add_text("Item with a ")
            builder.add_link("link", "https://example.com")
            builder.add_text(" and ")
            builder.add_bold_text("bold text")

        with builder.unordered_list():
            builder.add_paragraph("Nested item 1")
            builder.add_paragraph("Nested item 2")

    result = builder.to_str()
    assert "- Simple list item" in result
    assert "Item with a [link](https://example.com) and **bold text**" in result
    assert "  - Nested item 1" in result

    # Complex document
    builder = MarkdownBuilder()
    builder.add_heading(1, "My Project")
    builder.add_paragraph("A type-safe Markdown generator for Python")

    builder.add_heading(2, "Features")
    with builder.unordered_list():
        with builder.paragraph():
            builder.add_bold_text("Type-safe")
            builder.add_text(
                ": Uses Pydantic models to ensure valid Markdown structure"
            )

        builder.add_paragraph("Human-friendly automatic spacing and formatting")

    result = builder.to_str()
    assert "# My Project" in result
    assert "## Features" in result
    assert (
        "- **Type-safe**: Uses Pydantic models to ensure valid Markdown structure"
        in result
    )

    print("✓ Builder API tests passed!")


def test_advanced_examples():
    """Test advanced usage examples."""
    print("\nTesting advanced examples...")

    # Nested elements
    doc = Document(
        children=[
            Heading(level=1, content="Nested Example"),
            Blockquote(
                content=Document(
                    children=[
                        Paragraph(children=[Text(content="Quote with list:")]),
                        UnorderedList(
                            items=[
                                ListItem(
                                    content=Document(
                                        children=[
                                            Paragraph(children=[Text(content="Item 1")])
                                        ]
                                    )
                                ),
                                ListItem(
                                    content=Document(
                                        children=[
                                            Paragraph(children=[Text(content="Item 2")])
                                        ]
                                    )
                                ),
                            ]
                        ),
                    ]
                )
            ),
        ]
    )

    result = doc.to_str()
    assert "# Nested Example" in result
    assert "> Quote with list:" in result
    assert "> - Item 1" in result

    # Output example
    md = (
        markdown()
        .add_heading(1, "My Project")
        .add_paragraph("A type-safe Markdown generator for Python")
        .add_blockquote("The best way to create structured Markdown")
        .start_unordered_list()
        .add_paragraph("Type-safe with Pydantic")
        .add_paragraph("Fluent builder API")
        .add_paragraph("Nested element support")
        .end_unordered_list()
        .add_table(
            headers=["Feature", "Status"],
            rows=[
                ["Type safety", "✅"],
                ["Builder API", "✅"],
                ["Nested elements", "✅"],
            ],
            align=["left", "center"],
        )
        .to_str()
    )

    assert "# My Project" in md
    assert "> The best way to create structured Markdown" in md
    assert "- Type-safe with Pydantic" in md
    assert "| Feature | Status |" in md
    assert "| Type safety | ✅ |" in md

    print("✓ Advanced examples tests passed!")


def main():
    """Run all tests."""
    try:
        test_core_models()
        test_builder_api()
        test_advanced_examples()

        print("\n" + "=" * 50)
        print("✅ All code examples in README files are working correctly!")
        print("=" * 50)
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
