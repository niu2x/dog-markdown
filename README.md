# dog-markdown

一个用于 Python 的类型安全 Markdown 生成器，使用 Pydantic 构建。

A type-safe Markdown generator for Python, built with Pydantic.

## 特性 / Features

- **类型安全**: 使用 Pydantic 模型确保有效的 Markdown 结构
  - **Type-safe**: Uses Pydantic models to ensure valid Markdown structure
- **可扩展**: 轻松添加新的 Markdown 元素
  - **Extensible**: Easy to add new Markdown elements
- **人性化**: 自动间距和格式化
  - **Human-friendly**: Automatic spacing and formatting
- **嵌套元素**: 支持深度嵌套结构，如嵌套块引用
  - **Nested elements**: Supports deeply nested structures like nested blockquotes

## 支持的元素 / Supported Elements

- **文本**: 支持多行的纯文本
  - **Text**: Plain text with multi-line support
- **标题**: H1-H6 带级别参数
  - **Heading**: H1-H6 with level parameter
- **段落**: 组合文本、链接和图片，自动处理间距
  - **Paragraph**: Combines Text, Link, and Image with automatic spacing
- **链接**: 带有可选标题的超链接
  - **Link**: Hyperlinks with optional title
- **图片**: 带有替代文本、URL 和可选标题的图片
  - **Image**: Images with alt text, URL, and optional title
- **无序列表**: 支持嵌套内容的项目符号列表
  - **UnorderedList**: Bullet lists with support for nested content
- **代码块**: 带有可选语法高亮的代码块
  - **CodeBlock**: Code blocks with optional syntax highlighting
- **块引用**: 支持嵌套元素的引用文本
  - **Blockquote**: Quoted text that supports nested elements
- **表格**: 带有表头、行和可选对齐方式的表格
  - **Table**: Tables with headers, rows, and optional alignment

## 安装 / Installation

```bash
uv add dog-markdown
```

## 使用方法 / Usage

### 基础用法 / Basic Usage
```python
from dog_markdown import (
    Document, Heading, Paragraph, Text, Link, Image,
    UnorderedList, ListItem, CodeBlock, Blockquote, Table
)

# 创建文档 / Create a document
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

# 生成 Markdown / Generate Markdown
print(doc.to_str())
```

### 构建器 API / Builder API
```python
from dog_markdown import MarkdownBuilder

# 使用构建器创建文档 / Create document using builder
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

# 生成 Markdown / Generate Markdown
print(doc.to_str())
```

## 输出示例 / Output

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

- First item
- Second item with a [link](https://example.com)
```

## 开发 / Development

### 设置环境 / Setup

```bash
uv sync
```

### 测试 / Testing

```bash
uv run pytest
```

### 代码检查 / Linting

```bash
uv run ruff check .
```

### 代码格式化 / Formatting

```bash
uv run ruff format .
```

## 许可证 / License

MIT
