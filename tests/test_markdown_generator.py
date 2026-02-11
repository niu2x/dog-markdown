import pytest
from dog_markdown import (
    Document,
    Heading,
    Paragraph,
    Text,
    UnorderedList,
    ListItem,
    CodeBlock,
    Link,
    Image,
    Blockquote,
    Table,
)


class TestMarkdownGeneration:
    def test_text_to_str(self):
        text = Text(content="Hello world")
        assert text.to_str() == "Hello world"

        text = Text(content="Hello world\ndddd")
        assert text.to_str() == "Hello world\ndddd"

    def test_heading_to_str(self):
        heading = Heading(level=1, content="Main Title")
        assert heading.to_str() == "# Main Title"

        heading2 = Heading(level=3, content="Subsection")
        assert heading2.to_str() == "### Subsection"

    def test_paragraph_to_str(self):
        paragraph = Paragraph(
            children=[
                Text(content="This is "),
                Text(content=" and "),
                Text(content=" text."),
            ]
        )
        assert paragraph.to_str() == "This is  and  text."

    def test_paragraph_with_link_to_str(self):
        paragraph = Paragraph(
            children=[
                Text(content="Visit our "),
                Link(text="website", url="https://example.com"),
                Text(content=" for more information. You can also check our "),
                Link(
                    text="documentation",
                    url="https://docs.example.com",
                    title="Official Documentation",
                ),
                Text(content="."),
            ]
        )

        expected = (
            "Visit our [website](https://example.com) for more information. "
            'You can also check our [documentation](https://docs.example.com "Official Documentation").'
        )

        assert paragraph.to_str() == expected

    def test_link_to_str(self):
        link1 = Link(text="Google", url="https://google.com")
        assert link1.to_str() == "[Google](https://google.com)"

        link2 = Link(text="Example", url="https://example.com", title="Example Website")
        assert link2.to_str() == '[Example](https://example.com "Example Website")'

    def test_image_to_str(self):
        image1 = Image(alt="Dog picture", url="https://example.com/dog.jpg")
        assert image1.to_str() == "![Dog picture](https://example.com/dog.jpg)"

        image2 = Image(
            alt="Cat picture", url="https://example.com/cat.jpg", title="Cute cat"
        )
        assert (
            image2.to_str() == '![Cat picture](https://example.com/cat.jpg "Cute cat")'
        )

    def test_paragraph_with_image_to_str(self):
        paragraph = Paragraph(
            children=[
                Text(content="Check out our "),
                Image(alt="Product image", url="https://example.com/product.jpg"),
                Text(content=" or see our "),
                Image(
                    alt="Logo", url="https://example.com/logo.png", title="Company logo"
                ),
                Text(content="."),
            ]
        )

        expected = (
            "Check out our ![Product image](https://example.com/product.jpg) "
            'or see our ![Logo](https://example.com/logo.png "Company logo").'
        )

        assert paragraph.to_str() == expected

    def test_unordered_list_to_str(self):
        list_ = UnorderedList(
            items=[
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="First item")])]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Second item")])]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Third item")])]
                    )
                ),
            ]
        )
        assert list_.to_str() == "- First item\n- Second item\n- Third item"

        list2_ = UnorderedList(
            indent=2,
            items=[
                ListItem(
                    content=Document(
                        children=[
                            Paragraph(children=[Text(content="First item")]),
                            Paragraph(children=[Text(content="First item")]),
                        ]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Second item")])]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Third item")])]
                    )
                ),
            ],
        )
        assert (
            list2_.to_str()
            == "  - First item\n\n    First item\n\n  - Second item\n\n  - Third item"
        )

    def test_nested_list_to_str(self):
        nested_list = UnorderedList(
            items=[
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Parent item")])]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[
                            UnorderedList(
                                items=[
                                    ListItem(
                                        content=Document(
                                            children=[
                                                Paragraph(
                                                    children=[
                                                        Text(content="Child item 1")
                                                    ]
                                                )
                                            ]
                                        )
                                    ),
                                    ListItem(
                                        content=Document(
                                            children=[
                                                Paragraph(
                                                    children=[
                                                        Text(content="Child item 2")
                                                    ]
                                                )
                                            ]
                                        )
                                    ),
                                ]
                            )
                        ]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[
                            Paragraph(children=[Text(content="Another parent item")])
                        ]
                    )
                ),
            ]
        )

        expected = (
            "- Parent item\n\n"
            "  - Child item 1\n"
            "  - Child item 2\n\n"
            "- Another parent item"
        )

        assert nested_list.to_str() == expected

    def test_code_block_in_list_to_str(self):
        list_with_code = UnorderedList(
            items=[
                ListItem(
                    content=Document(
                        children=[Paragraph(children=[Text(content="Example code:")])]
                    )
                ),
                ListItem(
                    content=Document(
                        children=[
                            CodeBlock(content="print('hello')", language="python")
                        ]
                    )
                ),
            ]
        )

        expected = "- Example code:\n\n- ```python\n  print('hello')\n  ```"

        assert list_with_code.to_str() == expected

    def test_code_block_to_str(self):
        code = CodeBlock(content="print('hello world')", language="python")
        assert code.to_str() == "```python\nprint('hello world')\n```"

        code2 = CodeBlock(content="echo 'hello'")
        assert code2.to_str() == "```\necho 'hello'\n```"

    def test_blockquote_to_str(self):
        # Basic blockquote
        quote1 = Blockquote(
            content=Document(
                children=[Paragraph(children=[Text(content="This is a quote")])]
            )
        )
        assert quote1.to_str() == "> This is a quote"

        # Multi-line blockquote
        quote2 = Blockquote(
            content=Document(
                children=[
                    Paragraph(
                        children=[
                            Text(content="Line 1"),
                        ]
                    ),
                    Paragraph(
                        children=[
                            Text(content="Line 2"),
                        ]
                    ),
                    Paragraph(
                        children=[
                            Text(content="Line 3"),
                        ]
                    ),
                ]
            )
        )
        assert quote2.to_str() == "> Line 1\n>\n> Line 2\n>\n> Line 3"

        # Blockquote with Document content
        quote3 = Blockquote(
            content=Document(
                children=[
                    Paragraph(children=[Text(content="Nested quote")]),
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
        )

        expected_quote3 = "> Nested quote\n>\n> - Item 1\n> - Item 2"
        assert quote3.to_str() == expected_quote3

    def test_table_to_str(self):
        # Basic table
        table1 = Table(
            headers=["Name", "Age", "City"],
            rows=[["Alice", "30", "New York"], ["Bob", "25", "London"]],
        )

        expected_table1 = (
            "| Name | Age | City |\n"
            "| --- | --- | --- |\n"
            "| Alice | 30 | New York |\n"
            "| Bob | 25 | London |"
        )
        assert table1.to_str() == expected_table1

        # Table with alignment
        table2 = Table(
            headers=["Left", "Center", "Right"],
            rows=[["a", "b", "c"]],
            align=["left", "center", "right"],
        )

        expected_table2 = (
            "| Left | Center | Right |\n| --- | :---: | ---: |\n| a | b | c |"
        )
        assert table2.to_str() == expected_table2

        # Table with rich content
        table3 = Table(
            headers=["Item", "Link", "Image"],
            rows=[
                [
                    "Product",
                    Link(text="Website", url="https://example.com"),
                    Image(alt="Product image", url="https://example.com/img.jpg"),
                ]
            ],
        )

        expected_table3 = (
            "| Item | Link | Image |\n"
            "| --- | --- | --- |\n"
            "| Product | [Website](https://example.com) | ![Product image](https://example.com/img.jpg) |"
        )
        assert table3.to_str() == expected_table3

    def test_full_document_to_str(self):
        doc = Document(
            children=[
                Heading(level=1, content="My Document"),
                Paragraph(
                    children=[
                        Text(content="Welcome to my "),
                        Text(content=" . "),
                    ]
                ),
                UnorderedList(
                    items=[
                        ListItem(
                            content=Document(
                                children=[
                                    Paragraph(children=[Text(content="First feature")])
                                ]
                            )
                        ),
                        ListItem(
                            content=Document(
                                children=[
                                    Paragraph(children=[Text(content="Second feature")])
                                ]
                            )
                        ),
                        ListItem(
                            content=Document(
                                children=[
                                    Paragraph(children=[Text(content="Third feature")])
                                ]
                            )
                        ),
                    ]
                ),
                CodeBlock(content="def hello():\n    print('hi')", language="python"),
            ]
        )

        expected = (
            "# My Document\n\n"
            "Welcome to my  . \n\n"
            "- First feature\n"
            "- Second feature\n"
            "- Third feature\n\n"
            "```python\n"
            "def hello():\n"
            "    print('hi')\n"
            "```"
        )

        assert doc.to_str() == expected

        doc = Document(
            children=[
                Heading(level=1, content="My Document"),
                UnorderedList(
                    items=[
                        ListItem(
                            content=Document(
                                children=[
                                    Paragraph(
                                        children=[
                                            Text(content="Welcome to my\nxxxx"),
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                ),
            ]
        )

        expected = "# My Document\n\n- Welcome to my  \n  xxxx"

        assert doc.to_str() == expected

    def test_nested_blockquote_to_str(self):
        doc = Document(
            children=[
                Blockquote(
                    content=Document(
                        children=[
                            Paragraph(children=[Text(content="123")]),
                            Paragraph(children=[Text(content="123")]),
                            Blockquote(
                                content=Document(
                                    children=[
                                        Paragraph(children=[Text(content="123")]),
                                        Paragraph(children=[Text(content="123")]),
                                        CodeBlock(content="local a = 123\n b = a"),
                                    ]
                                )
                            ),
                        ]
                    )
                )
            ]
        )

        expected = (
            "> 123\n"
            ">\n"
            "> 123\n"
            ">\n"
            "> > 123\n"
            "> >\n"
            "> > 123\n"
            "> >\n"
            "> > ```\n"
            "> > local a = 123\n"
            "> >  b = a\n"
            "> > ```"
        )

        assert doc.to_str() == expected
