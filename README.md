# dog-markdown

A type-safe Markdown generator for Python, built with Pydantic.

## Features

- **Type-safe**: Uses Pydantic models to ensure valid Markdown structure
- **Extensible**: Easy to add new Markdown elements
- **Human-friendly**: Automatic spacing and formatting
- **Nested elements**: Supports deeply nested structures like nested blockquotes

## Supported Elements

- **Text**: Plain text with multi-line support
- **Heading**: H1-H6 with level parameter
- **Paragraph**: Combines Text, Link, and Image with automatic spacing
- **Link**: Hyperlinks with optional title
- **Image**: Images with alt text, URL, and optional title
- **UnorderedList**: Bullet lists with support for nested content
- **CodeBlock**: Code blocks with optional syntax highlighting
- **Blockquote**: Quoted text that supports nested elements
- **Table**: Tables with headers, rows, and optional alignment

## Installation

```bash
uv add dog-markdown
```

## Usage

```python
from dog_markdown import (
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
print(doc.to_str())
```

## Output

```markdown
# My Document

Welcome to dog-markdown! Check out our [website](https://example.com).

> This is a quote
>
> It supports nested elements

| Feature | Supported | Description |
| --- | :---: | --- |
| Type safety | ✓ | Uses Pydantic models |
| Nested elements | ✓ | Deeply nested structures |
| Tables | ✓ | With alignment support |
```

## Development

### Setup

```bash
uv sync
```

### Testing

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
```

### Formatting

```bash
uv run ruff format .
```

## License

MIT