import pytest
from dog_markdown import markdown, MarkdownBuilder


class TestMarkdownBuilder:
    def test_basic_document(self):
        builder = markdown()

        result = builder.add_heading(1, "Hello World")
        assert isinstance(result, MarkdownBuilder)  # Fluent interface

        builder.add_paragraph("This is a paragraph")
        builder.start_paragraph().add_text("This is another paragraph").end_paragraph()

        doc = builder.build()
        markdown_str = doc.to_str()

        assert "# Hello World" in markdown_str
        assert "This is a paragraph" in markdown_str
        assert "This is another paragraph" in markdown_str

        lines = [line.strip() for line in markdown_str.split("\n") if line.strip()]
        assert len(lines) == 3

    def test_procedural_paragraph(self):
        builder = markdown()

        from dog_markdown import Link, Text

        builder.add_paragraph(
            [
                Text(content="Welcome to "),
                Link(text="dog-markdown", url="https://example.com"),
                Text(content=". Check out our features:"),
            ]
        )

        assert "[dog-markdown](https://example.com)" in builder.to_str()

    def test_list_construction(self):
        builder = markdown()

        with builder.unordered_list():
            builder.add_paragraph("First item")
            builder.add_paragraph("Second item with nested content:")

            from dog_markdown import Link, Text

            with builder.paragraph():
                builder.add_text("This has ")
                builder.add_link("links", "https://example.com")
                builder.add_text(" and multiple lines")

        markdown_str = builder.to_str()
        assert "- First item" in markdown_str
        assert "- Second item with nested content:" in markdown_str
        assert (
            "- This has [links](https://example.com) and multiple lines" in markdown_str
        )

    def test_mixed_elements(self):
        builder = markdown()

        builder.add_heading(2, "Features")
        builder.add_code_block("def hello():\n    print('world')", "python")
        builder.add_blockquote(["Type-safe Markdown generation", "Built with Pydantic"])
        builder.start_paragraph()
        builder.add_image("Dog logo", "https://example.com/logo.png", "Company logo")
        builder.end_paragraph()

        markdown_str = builder.to_str()
        assert "## Features" in markdown_str
        assert "```python" in markdown_str
        assert "> Type-safe Markdown generation" in markdown_str
        assert (
            '![Dog logo](https://example.com/logo.png "Company logo")' in markdown_str
        )

    def test_table_construction(self):
        builder = markdown()

        builder.add_table(
            headers=["Feature", "Supported", "Description"],
            rows=[
                ["Type safety", "✓", "Uses Pydantic models"],
                ["Nested elements", "✓", "Deeply nested structures"],
                ["Tables", "✓", "With alignment support"],
            ],
            align=["left", "center", "left"],
        )

        markdown_str = builder.to_str()
        assert "| Feature | Supported | Description |" in markdown_str
        assert "| --- | :---: | --- |" in markdown_str
        assert "| Type safety | ✓ | Uses Pydantic models |" in markdown_str

    def test_direct_to_str(self):
        # Test that to_str() builds and returns the string directly
        result = (
            markdown()
            .add_heading(3, "Direct Test")
            .add_paragraph("This works directly!")
            .to_str()
        )

        assert "### Direct Test" in result
        assert "This works directly!" in result

    def test_nested_blockquote_with_builder(self):
        builder = markdown()

        # Create a nested blockquote using builder
        builder.add_blockquote("Outer quote")
        builder.add_blockquote(["Inner quote", "With multiple lines"])

        markdown_str = builder.to_str()
        assert "> Outer quote" in markdown_str
        assert "> Inner quote" in markdown_str
        assert "> With multiple lines" in markdown_str
