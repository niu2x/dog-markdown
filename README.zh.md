# dog-markdown

一个使用 Pydantic 构建的类型安全的 Python Markdown 生成器。

## 特性

- **类型安全**：使用 Pydantic 模型确保有效的 Markdown 结构
- **可扩展**：轻松添加新的 Markdown 元素
- **人性化**：自动处理间距和格式化
- **嵌套元素**：支持深度嵌套结构，如嵌套块引用

## 安装

```bash
uv add dog-markdown
```

## API 文档

### 核心模型 API

直接使用 Pydantic 模型创建结构化的 Markdown 文档。

#### Document

顶级文档容器，包含多个 Markdown 元素。

```python
from dog_markdown import Document, Heading, Paragraph, Text

doc = Document(
    children=[
        Heading(level=1, content="My Document"),
        Paragraph(children=[Text(content="Hello World!")])
    ]
)

print(doc.to_str())
```

**参数**:
- `children`: 文档包含的 Markdown 元素列表，支持 `Heading`, `Paragraph`, `UnorderedList`, `CodeBlock`, `Blockquote`, `Table`, `Document`

**方法**:
- `to_str()`: 将文档转换为 Markdown 字符串

#### Heading

标题元素，支持 H1-H9 级别。

```python
from dog_markdown import Heading

# 基础用法
heading = Heading(level=2, content="Section Title")

# 使用 Paragraph 作为内容（支持富文本）
from dog_markdown import Paragraph, Text, Link
heading = Heading(
    level=3,
    content=Paragraph(children=[
        Text(content="See our "),
        Link(text="API docs", url="/api"),
        Text(content=" for details")
    ])
)
```

**参数**:
- `level`: 标题级别 (1-9)
- `content`: 标题内容，支持字符串或 `Paragraph` 对象

#### Paragraph

段落元素，可包含文本、链接和图片。

```python
from dog_markdown import Paragraph, Text, Link, Image

# 基础文本段落
paragraph = Paragraph(children=[Text(content="Simple text paragraph")])

# 富文本段落
paragraph = Paragraph(children=[
    Text(content="Visit our "),
    Link(text="website", url="https://example.com"),
    Text(content=" or check out our "),
    Image(alt="Logo", url="/logo.png")
])
```

**参数**:
- `children`: 段落内容列表，支持 `Text`, `Link`, `Image`

#### Text

普通文本元素，支持加粗。

```python
from dog_markdown import Text

# 普通文本
text = Text(content="Plain text")

# 加粗文本
bold_text = Text(content="Important note", bold=True)
```

**参数**:
- `content`: 文本内容
- `bold`: 是否加粗 (默认: False)

#### Link

超链接元素。

```python
from dog_markdown import Link

# 基础链接
link = Link(text="Click me", url="https://example.com")

# 带标题的链接
link = Link(text="Download", url="/file.pdf", title="Download PDF document")
```

**参数**:
- `text`: 链接显示文本
- `url`: 目标 URL
- `title`: 可选，链接悬停时显示的标题

#### Image

图片元素，支持替代文本和标题。

```python
from dog_markdown import Image

# 基础图片
image = Image(alt="Cat picture", url="/cat.jpg")

# 带标题的图片
image = Image(alt="Dog picture", url="/dog.jpg", title="A cute dog")
```

**参数**:
- `alt`: 替代文本（无障碍支持）
- `url`: 图片 URL 或路径
- `title`: 可选，图片悬停时显示的标题

#### UnorderedList

无序列表（项目符号列表）。

```python
from dog_markdown import UnorderedList, ListItem, Document, Paragraph, Text

# 简单列表
list = UnorderedList(
    items=[
        ListItem(content=Document(children=[Paragraph(children=[Text(content="Item 1")])])),
        ListItem(content=Document(children=[Paragraph(children=[Text(content="Item 2")])]))
    ]
)

# 嵌套列表
nested_list = UnorderedList(
    items=[
        ListItem(content=Document(children=[
            Paragraph(children=[Text(content="Parent item")]),
            UnorderedList(
                items=[
                    ListItem(content=Document(children=[Paragraph(children=[Text(content="Child item 1")])])),
                    ListItem(content=Document(children=[Paragraph(children=[Text(content="Child item 2")])]))
                ]
            )
        ]))
    ]
)
```

**参数**:
- `items`: 列表项 `ListItem` 对象列表
- `indent`: 缩进级别 (默认: 1)

#### ListItem

列表项元素。

```python
from dog_markdown import ListItem, Document, Paragraph, Text

list_item = ListItem(
    content=Document(children=[Paragraph(children=[Text(content="List item content")])])
)
```

**参数**:
- `content`: 列表项内容，`Document` 对象

#### CodeBlock

代码块元素，支持语法高亮。

```python
from dog_markdown import CodeBlock

# 基础代码块
code_block = CodeBlock(content="print('Hello World')")

# 带语法高亮的代码块
python_code = CodeBlock(
    content="def add(a, b):\n    return a + b",
    language="python"
)
```

**参数**:
- `content`: 代码内容
- `language`: 可选，编程语言名称（用于语法高亮）

#### Blockquote

块引用元素，支持嵌套。

```python
from dog_markdown import Blockquote, Document, Paragraph, Text

# 基础引用
quote = Blockquote(
    content=Document(children=[Paragraph(children=[Text(content="To be or not to be")])])
)

# 嵌套引用
nested_quote = Blockquote(
    content=Document(children=[
        Paragraph(children=[Text(content="Outer quote")]),
        Blockquote(
            content=Document(children=[Paragraph(children=[Text(content="Inner quote")])])
        )
    ])
)
```

**参数**:
- `content`: 引用内容，`Document` 对象

#### Table

表格元素，支持列对齐。

```python
from dog_markdown import Table

# 基础表格
table = Table(
    headers=["Name", "Age", "Email"],
    rows=[
        ["Alice", "30", "alice@example.com"],
        ["Bob", "25", "bob@example.com"]
    ]
)

# 带对齐的表格
table = Table(
    headers=["Name", "Age", "Email"],
    rows=[
        ["Alice", "30", "alice@example.com"],
        ["Bob", "25", "bob@example.com"]
    ],
    align=["left", "center", "right"]
)

# 富文本表格
table = Table(
    headers=["Product", "Link", "Image"],
    rows=[
        [
            "Laptop",
            Link(text="Buy now", url="/laptop"),
            Image(alt="Laptop", url="/laptop.jpg")
        ]
    ]
)
```

**参数**:
- `headers`: 表格列头列表
- `rows`: 表格行数据列表，每个单元格支持字符串、`Text`, `Link`, `Image`
- `align`: 可选，列对齐方式列表，支持 `left`, `center`, `right`，默认左对齐

### Builder API

使用流畅的链式调用 API 构建 Markdown 文档，更适合程序化创建。

#### 基础用法

```python
from dog_markdown import MarkdownBuilder

builder = MarkdownBuilder()
doc = builder
    .add_heading(1, "My Document")
    .add_paragraph("Welcome to dog-markdown!")
    .add_code_block("print('Hello World')", language="python")
    .build()

print(doc.to_str())
```

#### 快捷创建

使用 `markdown()` 函数快速创建 Builder:

```python
from dog_markdown import markdown

doc = markdown()
    .add_heading(2, "Quick Start")
    .add_paragraph("Easy to use builder API")
    .to_str()
```

#### 富文本段落

```python
# 基础用法
builder.add_paragraph([
    "Visit our ",
    builder.link("website", "https://example.com"),
    " for more info"
])

# 使用上下文管理器创建复杂段落
with builder.paragraph():
    builder.add_bold_text("Note:")
    builder.add_text(" This is a ")
    builder.add_bold_text("very important")
    builder.add_text(" message with ")
    builder.add_link("links", "https://example.com")
```

#### 列表操作

使用 `add_paragraph` 直接在列表中添加段落，简化 API 使用:

```python
# 使用上下文管理器创建列表
with builder.unordered_list():
    # 简单列表项
    builder.add_paragraph("Simple list item")
    
    # 富文本列表项
    with builder.paragraph():
        builder.add_text("Item with a ")
        builder.add_link("link", "https://example.com")
        builder.add_text(" and ")
        builder.add_bold_text("bold text")
    
    # 复杂列表项（包含多个段落）
    with builder.paragraph():
        builder.add_bold_text("Multi-paragraph item:")
    builder.add_paragraph("This is the first paragraph")
    builder.add_paragraph("This is the second paragraph")
    
    # 嵌套列表
    with builder.unordered_list():
        builder.add_paragraph("Nested item 1")
        builder.add_paragraph("Nested item 2")
```

#### 复杂文档示例

```python
from dog_markdown import MarkdownBuilder

builder = MarkdownBuilder()

# 创建文档标题和描述
builder.add_heading(1, "My Project")
builder.add_paragraph("A type-safe Markdown generator for Python")

# 添加特性列表
builder.add_heading(2, "Features")
with builder.unordered_list():
    with builder.paragraph():
        builder.add_bold_text("Type-safe")
        builder.add_text(": Uses Pydantic models to ensure valid Markdown structure")
    
    with builder.paragraph():
        builder.add_bold_text("Extensible")
        builder.add_text(": Easy to add new Markdown elements")
    
    builder.add_paragraph("Human-friendly automatic spacing and formatting")

# 添加代码示例
builder.add_heading(2, "Example")
builder.add_code_block(
    "def hello():\n    print('Hello World!')",
    language="python"
)

# 添加引用
builder.add_blockquote([
    "This is a blockquote",
    builder.paragraph("It supports multiple paragraphs and "),
    builder.paragraph(["even ", builder.bold_text("bold text"), " or ", builder.link("links", "https://example.com")])
])

# 添加表格
builder.add_table(
    headers=["Feature", "Supported", "Description"],
    rows=[
        ["Type safety", "✓", "Uses Pydantic models"],
        ["Nested elements", "✓", "Deeply nested structures"],
        ["Tables", "✓", "With alignment support"]
    ],
    align=["left", "center", "left"]
)

# 输出结果
print(builder.to_str())
```

#### Builder 方法参考

##### 文档结构

- `add_heading(level: int, content: str | Paragraph)`: 添加标题
- `add_paragraph(content: str | List[str | Text | Link | Image] | Paragraph)`: 添加段落
- `add_code_block(content: str, language: str | None = None)`: 添加代码块
- `add_blockquote(content: str | Document | List[...])`: 添加块引用
- `add_table(headers: List[str], rows: List[List[...]], align: List[str | None] | None = None)`: 添加表格
- `build()`: 构建并返回 `Document` 对象
- `to_str()`: 直接生成并返回 Markdown 字符串

##### 列表操作

- `start_unordered_list()`: 开始无序列表
- `end_unordered_list()`: 结束当前无序列表
- `unordered_list()`: 返回列表上下文管理器

##### 上下文管理器

- `paragraph()`: 段落上下文管理器，用于创建复杂富文本段落
- `unordered_list()`: 列表上下文管理器，用于创建各级列表

##### 文本元素

- `add_link(text: str, url: str, title: str | None = None)`: 创建链接元素（用于在段落中嵌套）
- `add_image(alt: str, url: str, title: str | None = None)`: 创建图片元素（用于在段落中嵌套）
- `add_text(content: str)`: 创建普通文本元素（用于在段落中嵌套）
- `add_bold_text(content: str)`: 创建加粗文本元素（用于在段落中嵌套）

## 高级用法

### 嵌套元素

```python
from dog_markdown import Document, Heading, Blockquote, Paragraph, Text, UnorderedList, ListItem

doc = Document(
    children=[
        Heading(level=1, content="Nested Example"),
        Blockquote(
            content=Document(
                children=[
                    Paragraph(children=[Text(content="Quote with list:")]),
                    UnorderedList(
                        items=[
                            ListItem(content=Document(children=[Paragraph(children=[Text(content="Item 1")])])),
                            ListItem(content=Document(children=[Paragraph(children=[Text(content="Item 2")])]))
                        ]
                    )
                ]
            )
        )
    ]
)
```

### 生成复杂文档

结合 Builder API 的上下文管理器可以创建非常复杂的文档结构:

```python
from dog_markdown import MarkdownBuilder

builder = MarkdownBuilder()

# 创建技术文档
builder.add_heading(1, "API Documentation")

builder.add_heading(2, "Introduction")
builder.add_paragraph("Welcome to our API documentation. This guide will help you get started.")

builder.add_heading(2, "Getting Started")
with builder.unordered_list():
    builder.add_paragraph("Sign up for an API key")
    builder.add_paragraph("Install the SDK")
    builder.add_paragraph("Make your first request")

builder.add_heading(3, "Authentication")
builder.add_paragraph("Authenticate your requests using API keys in the Authorization header.")
builder.add_code_block(
    "import requests\n\nheaders = {\n    'Authorization': 'Bearer YOUR_API_KEY'\n}\n\nresponse = requests.get('https://api.example.com/data', headers=headers)",
    language="python"
)

builder.add_heading(2, "Endpoints")

with builder.unordered_list():
    with builder.paragraph():
        builder.add_bold_text("GET /api/data")
        builder.add_text(": Retrieve data from the server")
    
    with builder.paragraph():
        builder.add_bold_text("POST /api/data")
        builder.add_text(": Create new data on the server")
    
    with builder.paragraph():
        builder.add_bold_text("PUT /api/data/{id}")
        builder.add_text(": Update existing data")

print(builder.to_str())
```

## 输出示例

以下代码:

```python
from dog_markdown import markdown

md = markdown()
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
            ["Nested elements", "✅"]
        ],
        align=["left", "center"]
    )
    .to_str()

print(md)
```

将生成:

```markdown
# My Project

A type-safe Markdown generator for Python

> The best way to create structured Markdown

- Type-safe with Pydantic
- Fluent builder API
- Nested element support

| Feature | Status |
| --- | :---: |
| Type safety | ✅ |
| Builder API | ✅ |
| Nested elements | ✅ |
```

## 开发

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

## 许可证

MIT