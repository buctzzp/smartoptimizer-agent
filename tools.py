"""LLM-callable tools for the agent.

Only `generate_pdf` — the LLM handles all analysis itself
and uses this tool to persist the report as a downloadable file.
"""

import os
from datetime import datetime


_CIK_CSS = """\
body { font-family: 'STHeiti Light', 'Noto Sans CJK SC', 'Noto Sans SC', 'WenQuanYi Micro Hei', sans-serif; }
code, pre { font-family: 'STHeiti Light', 'Noto Sans CJK SC', 'Noto Sans SC', 'WenQuanYi Micro Hei', 'Courier New', monospace; }
"""


def generate_pdf(content: str, output_dir: str = "outputs/reports") -> dict:
    """Convert markdown content to PDF and return the file path."""
    from markdown_pdf import MarkdownPdf, Section

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"smartoptimizer_report_{timestamp}.pdf"
    path = os.path.join(output_dir, filename)

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(content), user_css=_CIK_CSS)
    pdf.save(path)

    return {"path": path, "filename": filename}

