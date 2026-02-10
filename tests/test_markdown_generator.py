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
)


class TestMarkdownGeneration:
    def test_text_to_str(self):
        text = Text(content="Hello world")
        assert text.to_str() == "Hello world"

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
        assert list_.to_str() == "- First item\n\n- Second item\n\n- Third item"

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
            "  - Child item 1\n\n"
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

    def test_full_document_to_str(self):
        doc = Document(
            children=[
                Heading(level=1, content="My Document"),
                Paragraph(
                    children=[
                        Text(content="Welcome to my "),
                        Text(content="."),
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
            "Welcome to my .\n\n"
            "- First feature\n\n"
            "- Second feature\n\n"
            "- Third feature\n\n"
            "```python\n"
            "def hello():\n"
            "    print('hi')\n"
            "```"
        )

        assert doc.to_str() == expected
