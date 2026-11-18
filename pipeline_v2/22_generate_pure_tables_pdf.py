#!/usr/bin/env python3
"""
=============================================================================
PHASE 8: PURE TABLES PDF GENERATOR
Delhi-NCR Circular Plastic Assessment
=============================================================================
Creates a standalone PDF containing ONLY the 6 elite tables, stripped of 
any introductory text or manuscript prose, exactly as requested for review.
=============================================================================
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TABLES_FILE = BASE / "Delhi_NCT_Elite_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCT_Pure_Tables_Annex.pdf"

def generate_pure_tables():
    print("Compiling Pure Tables PDF...")
    
    with open(TABLES_FILE, 'r', encoding='utf-8') as f:
        tables_content = f.read()
        
    # Strip out the first introductory paragraphs from the tables markdown
    # The markdown starts with an H1 and some text before the first H2 (Table 1)
    # We will split at "## Table 1" and only keep everything from there onwards
    parts = tables_content.split("## Table 1:", 1)
    if len(parts) > 1:
        pure_tables_markdown = "## Table 1:" + parts[1]
    else:
        pure_tables_markdown = tables_content
        
    # Convert to HTML
    html_content = markdown.markdown(pure_tables_markdown, extensions=['tables'])
    
    # CSS for academic styling
    css = CSS(string='''
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.5; color: #333; }
        h2 { font-size: 14pt; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; color: #111; page-break-before: auto; }
        p { margin-bottom: 15px; text-align: justify; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; page-break-inside: avoid; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 9pt; }
        th { background-color: #f8f9fa; font-weight: bold; }
        tr:nth-child(even) { background-color: #fcfcfc; }
        blockquote { font-style: italic; color: #555; border-left: 4px solid #ccc; padding-left: 10px; margin: 15px 0; font-size: 10pt; background: #f9f9f9; padding-top: 5px; padding-bottom: 5px; }
    ''')
    
    # Write PDF
    HTML(string=html_content, base_url=str(BASE)).write_pdf(PDF_FILE, stylesheets=[css])
    print(f"✓ Pure Tables PDF generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_pure_tables()
