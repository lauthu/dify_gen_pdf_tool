import os
import pytest
from tools.gen_pdf import markdown_to_pdf

def test_markdown_to_pdf(tmp_path):
    # Create a test markdown file with Chinese content
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
    
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    
    # Write test markdown content
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Convert to PDF
    markdown_to_pdf(str(input_file), str(output_file))
    
    # Check if PDF was created and has size greater than 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_markdown_to_pdf_with_custom_css(tmp_path):
    # Create a test CSS file
    css_content = """
    body { font-family: Arial, sans-serif; }
    h1 { color: blue; }
    """
    
    css_file = tmp_path / "custom.css"
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # Create a simple markdown file
    md_content = "# Test Heading\n\nTest content"
    input_file = tmp_path / "test.md"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    output_file = tmp_path / "test_custom.pdf"
    
    # Convert to PDF with custom CSS
    markdown_to_pdf(str(input_file), str(output_file), css_content)
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_markdown_to_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        markdown_to_pdf("nonexistent.md", "output.pdf")
