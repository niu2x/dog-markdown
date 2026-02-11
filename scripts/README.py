from dog_markdown import MarkdownBuilder

builder = MarkdownBuilder()

# Title
builder.add_heading(1, "dog-markdown")

# Description
builder.add_paragraph("A type-safe Markdown generator for Python, built with Pydantic.")

# Features
builder.add_heading(2, "Features")

with builder.unordered_list():
    with builder.paragraph():
        builder.add_bold_text("Type-safe")
        builder.add_text(": Uses Pydantic models to ensure valid Markdown structure")

    with builder.paragraph():
        builder.add_bold_text("Extensible")
        builder.add_text(": Easy to add new Markdown elements")

    with builder.paragraph():
        builder.add_bold_text("Human-friendly")
        builder.add_text(": Automatic spacing and formatting")

    with builder.paragraph():
        builder.add_bold_text("Nested elements")
        builder.add_text(": Supports deeply nested structures like nested blockquotes")

# Supported Elements
builder.add_heading(2, "Supported Elements")

with builder.unordered_list():
    with builder.paragraph():
        builder.add_bold_text("Text")
        builder.add_text(": Plain text with multi-line support")

    with builder.paragraph():
        builder.add_bold_text("Heading")
        builder.add_text(": H1-H6 with level parameter")

    with builder.paragraph():
        builder.add_bold_text("Paragraph")
        builder.add_text(": Combines Text, Link, and Image with automatic spacing")

    with builder.paragraph():
        builder.add_bold_text("Link")
        builder.add_text(": Hyperlinks with optional title")

    with builder.paragraph():
        builder.add_bold_text("Image")
        builder.add_text(": Images with alt text, URL, and optional title")

    with builder.paragraph():
        builder.add_bold_text("UnorderedList")
        builder.add_text(": Bullet lists with support for nested content")

    with builder.paragraph():
        builder.add_bold_text("CodeBlock")
        builder.add_text(": Code blocks with optional syntax highlighting")

    with builder.paragraph():
        builder.add_bold_text("Blockquote")
        builder.add_text(": Quoted text that supports nested elements")

    with builder.paragraph():
        builder.add_bold_text("Table")
        builder.add_text(": Tables with headers, rows, and optional alignment")

# Installation
builder.add_heading(2, "Installation")
builder.add_code_block("uv add dog-markdown", language="bash")

# Usage
builder.add_heading(2, "Usage")

builder.add_heading(3, "Basic Usage")
basic_usage_code = """from dog_markdown import (
    Document, Heading, Paragraph, Text, Link, Image,
    UnorderedList, ListItem, CodeBlock, Blockquote, Table
)

# Create a document
doc = Document(children=[
    Heading(level=1, content="My Document"),
    Paragraph(children=[
        Text(content="Welcome to dog-markdown! Check out our "),
        Link(text="website", url="https://example.com"),
        Text(content=".")
    ]),
    Blockquote(content=Document(children=[
        Paragraph(children=[Text(content="This is a quote")]),
        Paragraph(children=[Text(content="It supports nested elements")])
    ])),
    Table(
        headers=["Feature", "Supported", "Description"],
        rows=[
            ["Type safety", "✓", "Uses Pydantic models"],
            ["Nested elements", "✓", "Deeply nested structures"],
            ["Tables", "✓", "With alignment support"]
        ],
        align=["left", "center", "left"]
    )
])

# Generate Markdown
print(doc.to_str())"""
builder.add_code_block(basic_usage_code, language="python")

builder.add_heading(3, "Builder API")
builder_api_code = """from dog_markdown import MarkdownBuilder

# Create document using builder
builder = MarkdownBuilder()
doc = builder\
    .add_heading(1, "My Document")\
    .add_paragraph([
        "Welcome to dog-markdown! Check out our ",
        builder.link("website", "https://example.com"),
        "."
    ])\
    .add_blockquote([
        "This is a quote",
        builder.paragraph("It supports nested elements")
    ])\
    .start_list()\
        .add_list_item("First item")\
        .add_list_item([
            "Second item with a ",
            builder.link("link", "https://example.com")
        ])\
    .end_list()\
    .build()

# Generate Markdown
print(doc.to_str())"""
builder.add_code_block(builder_api_code, language="python")

# Output
builder.add_heading(2, "Output")
output_md = """# My Document

Welcome to dog-markdown! Check out our [website](https://example.com).

> This is a quote
>
> It supports nested elements

| Feature | Supported | Description |
| --- | :---: | --- |
| Type safety | ✓ | Uses Pydantic models |
| Nested elements | ✓ | Deeply nested structures |
| Tables | ✓ | With alignment support |

- First item
- Second item with a [link](https://example.com)"""
builder.add_code_block(output_md, language="markdown")

# Development
builder.add_heading(2, "Development")

builder.add_heading(3, "Setup")
builder.add_code_block("uv sync", language="bash")

builder.add_heading(3, "Testing")
builder.add_code_block("uv run pytest", language="bash")

builder.add_heading(3, "Linting")
builder.add_code_block("uv run ruff check .", language="bash")

builder.add_heading(3, "Formatting")
builder.add_code_block("uv run ruff format .", language="bash")

# License
builder.add_heading(2, "License")
builder.add_paragraph("MIT")

# Generate and print the result
print(builder.to_str())
