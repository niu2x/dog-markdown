# dog-markdown

一个用于 Python 的类型安全 Markdown 生成器，使用 Pydantic 构建。

## 特性

- **类型安全**: 使用 Pydantic 模型确保有效的 Markdown 结构
- **可扩展**: 轻松添加新的 Markdown 元素
- **人性化**: 自动间距和格式化
- **嵌套元素**: 支持深度嵌套结构，如嵌套块引用

## 支持的元素

- **文本**: 支持多行的纯文本
- **标题**: H1-H6 带级别参数
- **段落**: 组合文本、链接和图片，自动处理间距
- **链接**: 带有可选标题的超链接
- **图片**: 带有替代文本、URL 和可选标题的图片
- **无序列表**: 支持嵌套内容的项目符号列表
- **代码块**: 带有可选语法高亮的代码块
- **块引用**: 支持嵌套元素的引用文本
- **表格**: 带有表头、行和可选对齐方式的表格

## 安装

```bash
uv add dog-markdown
```

## 使用方法

### 基础用法
```python
from dog_markdown import (
    Document, Heading, Paragraph, Text, Link, Image,
    UnorderedList, ListItem, CodeBlock, Blockquote, Table
)

# 创建文档
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

# 生成 Markdown
print(doc.to_str())
```

### 构建器 API
```python
from dog_markdown import MarkdownBuilder

# 使用构建器创建文档
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

# 生成 Markdown
print(doc.to_str())
```

## 输出示例

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

## 开发

### 设置环境

```bash
uv sync
```

### 测试

```bash
uv run pytest
```

### 代码检查

```bash
uv run ruff check .
```

### 代码格式化

```bash
uv run ruff format .
```

## 许可证

MIT