import base64
from unittest.mock import MagicMock
from tools.gen_pdf import GeneratePDFTool


def test_generate_pdf_with_markdown():
    """Test PDF generation from markdown content"""
    tool = GeneratePDFTool()

    # Test markdown content
    md_content = """# Test Title

## Subtitle

This is a test paragraph with **bold** and *italic* text.

* List item 1
* List item 2

1. Numbered item 1
2. Numbered item 2

> This is a blockquote

---

[Link text](https://example.com)
"""

    tool_parameters = {'data': md_content}

    # Get the result from the generator
    results = list(tool._invoke(tool_parameters))

    # Should return exactly one message
    assert len(results) == 1

    # Check that it's a blob message with PDF mime type
    message = results[0]
    assert hasattr(message, 'blob')
    assert message.meta.get('mime_type') == 'application/pdf'

    # Verify the blob is valid base64
    try:
        pdf_data = base64.b64decode(message.blob)
        assert len(pdf_data) > 0
        # PDF files start with %PDF
        assert pdf_data.startswith(b'%PDF')
    except Exception as e:
        assert False, f"Invalid base64 or PDF data: {e}"


def test_generate_pdf_empty_data():
    """Test handling of empty markdown content"""
    tool = GeneratePDFTool()
    tool_parameters = {'data': ''}

    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'text')
    assert "No data provided" in message.text


def test_generate_pdf_no_data_parameter():
    """Test handling of missing data parameter"""
    tool = GeneratePDFTool()
    tool_parameters = {}

    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'text')
    assert "No data provided" in message.text


def test_generate_pdf_with_chinese_content():
    """Test PDF generation with Chinese characters"""
    tool = GeneratePDFTool()

    md_content = """# 测试标题

## 副标题

这是一段中文测试文本。

* 列表项 1
* 列表项 2

**粗体文字** 和 *斜体文字*
"""

    tool_parameters = {'data': md_content}
    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'blob')
    assert message.meta.get('mime_type') == 'application/pdf'


def test_generate_pdf_with_table():
    """Test PDF generation with markdown table"""
    tool = GeneratePDFTool()

    md_content = """# Table Test

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
"""

    tool_parameters = {'data': md_content}
    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'blob')
    assert message.meta.get('mime_type') == 'application/pdf'


def test_generate_pdf_with_code_block():
    """Test PDF generation with code blocks"""
    tool = GeneratePDFTool()

    md_content = """# Code Example

```python
def hello():
    print("Hello, World!")
```

Inline `code` example.
"""

    tool_parameters = {'data': md_content}
    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'blob')
    assert message.meta.get('mime_type') == 'application/pdf'


def test_generate_pdf_invalid_data_type():
    """Test handling of invalid data type"""
    tool = GeneratePDFTool()
    tool_parameters = {'data': 123}  # Not a string

    results = list(tool._invoke(tool_parameters))

    assert len(results) == 1
    message = results[0]
    assert hasattr(message, 'text')
    assert "Invalid input" in message.text
