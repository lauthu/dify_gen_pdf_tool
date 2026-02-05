#!/usr/bin/env python3
import markdown
import base64
from weasyprint import HTML
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


DEFAULT_CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap');

body {
    font-family: 'Noto Sans SC', sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1, h2, h3, h4, h5, h6 {
    color: #333;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.3em; }

p {
    margin: 1em 0;
    text-align: justify;
}

a {
    color: #0366d6;
    text-decoration: none;
}

code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: monospace;
}

blockquote {
    border-left: 4px solid #ddd;
    padding-left: 1em;
    margin-left: 0;
    color: #666;
}

hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
}

ul, ol {
    padding-left: 2em;
    margin: 0.5em 0;
}

li {
    margin: 0.5em 0;
}

li ul, li ol {
    margin: 0.2em 0;
}

li > ul > li, li > ol > li {
    margin: 0.2em 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f6f8fa;
}
'''



class GeneratePDFTool(Tool):

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        Convert Markdown content to PDF.

        Args:
            tool_parameters: Dictionary containing 'data' key with markdown content

        Yields:
            ToolInvokeMessage: PDF blob message or error text message
        """
        try:
            data = tool_parameters.get('data', '')

            if not data:
                yield self.create_text_message("No data provided.")
                return

            # Validate input is a string
            if not isinstance(data, str):
                yield self.create_text_message("Invalid input: data must be a string.")
                return

            # Convert markdown to HTML
            html_content = markdown.markdown(
                data,
                extensions=[
                    'tables',
                    'fenced_code',
                    'footnotes',
                    'markdown.extensions.sane_lists',
                    'markdown.extensions.nl2br'
                ]
            )

            # Wrap HTML content with proper document structure
            html_doc = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        {DEFAULT_CSS}
    </style>
</head>
<body>
    {html_content}
</body>
</html>'''

            # Convert HTML to PDF and get the PDF as bytes
            pdf_bytes = HTML(string=html_doc).write_pdf()

            # Convert PDF bytes to base64 string
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

            # Yield the PDF as a blob message
            yield self.create_blob_message(pdf_base64, meta={"mime_type": "application/pdf"})

        except Exception as e:
            yield self.create_text_message(f"Error converting markdown to PDF: {str(e)}")