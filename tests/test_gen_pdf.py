import os
import pytest
import base64
from unittest.mock import Mock
from tools.gen_pdf import GeneratePDFTool


def create_mock_tool():
    """Create a mock tool instance with required dependencies."""
    mock_runtime = Mock()
    mock_session = Mock()
    tool = GeneratePDFTool(runtime=mock_runtime, session=mock_session)
    return tool


def test_generate_pdf_tool():
    """Test the GeneratePDFTool with basic markdown content."""
    # Create a test markdown content with Chinese content
    md_content = """# 测试标题

## 副标题

这是一段中文测试文本。

* 列表项 1
* 列表项 2

1. 编号列表 1
2. 编号列表 2

> 这是一段引用文字

---

**粗体文字** 和 *斜体文字*

[链接文字](https://example.com)
"""

    # Create tool instance
    tool = create_mock_tool()

    # Invoke the tool
    result = list(tool._invoke({'data': md_content}))

    # Check that we got a result
    assert len(result) > 0

    # Get the message
    message = result[0]

    # Check that it's a blob message with PDF mime type
    assert hasattr(message, 'meta')
    assert message.meta.get('mime_type') == 'application/pdf'

    # Check that we have valid base64 encoded PDF data
    assert hasattr(message, 'message')
    assert hasattr(message.message, 'blob')
    pdf_data = base64.b64decode(message.message.blob)
    assert pdf_data.startswith(b'%PDF')  # PDF files start with this signature


def test_generate_pdf_tool_empty_data():
    """Test the GeneratePDFTool with empty data."""
    tool = create_mock_tool()

    result = list(tool._invoke({'data': ''}))

    # Should get a text message about no data
    assert len(result) > 0


def test_generate_pdf_tool_complex_markdown():
    """Test the GeneratePDFTool with complex markdown including tables."""
    md_content = """# Test Document

## Table Example

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Code Block

```python
def hello_world():
    print("Hello, World!")
```

## Nested Lists

- Item 1
  - Nested 1.1
  - Nested 1.2
    - Deep nested 1.2.1
- Item 2
"""

    tool = create_mock_tool()
    result = list(tool._invoke({'data': md_content}))

    assert len(result) > 0
    message = result[0]
    assert hasattr(message, 'meta')
    assert message.meta.get('mime_type') == 'application/pdf'

    # Verify it's a valid PDF
    assert hasattr(message, 'message')
    assert hasattr(message.message, 'blob')
    pdf_data = base64.b64decode(message.message.blob)
    assert pdf_data.startswith(b'%PDF')
    assert len(pdf_data) > 0
