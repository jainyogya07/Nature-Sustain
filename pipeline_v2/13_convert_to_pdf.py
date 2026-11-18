#!/usr/bin/env python3
"""
=============================================================================
Convert Markdown to PDF using Markdown and WeasyPrint
=============================================================================
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MD_FILE = BASE / "FINAL_MANUSCRIPT.md"
PDF_FILE = BASE / "Delhi_NCR_Circular_Plastic_FINAL_MANUSCRIPT.pdf"

def md_to_pdf():
    print("Converting Markdown to PDF...")
    
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    html_body = markdown.markdown(md_text, extensions=['extra', 'tables'])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Final Manuscript</title>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    css = CSS(string='''
        @page { size: A4; margin: 2.5cm; }
        body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.6; color: #333; }
        h1 { font-size: 18pt; color: #2C3E50; text-align: center; margin-bottom: 30px; }
        h2 { font-size: 14pt; color: #34495E; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 25px; }
        h3 { font-size: 12pt; color: #2C3E50; margin-top: 20px; }
        p { margin-bottom: 15px; text-align: justify; }
        ul { margin-bottom: 15px; }
        li { margin-bottom: 5px; }
        strong { color: #2C3E50; }
        hr { border: 0; border-top: 1px solid #ccc; margin: 20px 0; }
    ''')
    
    HTML(string=html_content).write_pdf(str(PDF_FILE), stylesheets=[css])
    print(f"✓ PDF successfully generated: {PDF_FILE}")

if __name__ == "__main__":
    md_to_pdf()
