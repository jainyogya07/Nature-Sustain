#!/usr/bin/env python3
"""
=============================================================================
PHASE 8: FULL MANUSCRIPT PDF GENERATOR
Delhi-NCR Circular Plastic Assessment
=============================================================================
Compiles the prose, the visual figures, and the 6 elite tables into 
a single, unified high-impact manuscript PDF.
=============================================================================
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROSE_FILE = BASE / "FINAL_MANUSCRIPT_PROSE.md"
TABLES_FILE = BASE / "Delhi_NCT_Elite_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCT_Elite_Full_Manuscript.pdf"
ASSETS_DIR = BASE / "pipeline_v2" / "visual_assets"

def generate_full_pdf():
    print("Compiling full manuscript (Prose + Figures + Tables)...")
    
    # 1. Read Prose
    with open(PROSE_FILE, 'r', encoding='utf-8') as f:
        prose_content = f.read()
        
    # 2. Add Visual Figures Section
    figures_content = "\n\n## 5. Visual Figures\n\n"
    figures_content += "### Figure 1: Socio-Spatial Inequality\n"
    figures_content += f"![Figure 1](file://{ASSETS_DIR}/Fig1_SocioSpatial_Inequality.png)\n\n"
    
    figures_content += "### Figure 2: Intervention Priority Stability\n"
    figures_content += f"![Figure 2](file://{ASSETS_DIR}/Fig2_Intervention_Stability.png)\n\n"
    
    figures_content += "### Figure 3: Economic Diversion Scenario\n"
    figures_content += f"![Figure 3](file://{ASSETS_DIR}/Fig3_Economic_Diversion.png)\n\n"
    
    # 3. Read Tables
    with open(TABLES_FILE, 'r', encoding='utf-8') as f:
        tables_content = f.read()
        
    # Replace the duplicate main header from the tables file to make it flow better
    tables_content = tables_content.replace("# Elite Empirical Evidence Tables: Delhi NCT Circular Plastic Waste\n\n", "## 6. Elite Empirical Evidence Tables\n\n")
    
    # 4. Combine all
    full_markdown = prose_content + figures_content + tables_content
    
    # Convert to HTML
    html_content = markdown.markdown(full_markdown, extensions=['tables'])
    
    # CSS for academic styling
    css = CSS(string='''
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.5; color: #333; }
        h1 { font-size: 18pt; text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-top: 0; }
        h2 { font-size: 14pt; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; color: #111; }
        h3 { font-size: 12pt; margin-top: 20px; color: #222; }
        p { margin-bottom: 15px; text-align: justify; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; page-break-inside: avoid; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 9pt; }
        th { background-color: #f8f9fa; font-weight: bold; }
        tr:nth-child(even) { background-color: #fcfcfc; }
        blockquote { font-style: italic; color: #555; border-left: 4px solid #ccc; padding-left: 10px; margin: 15px 0; font-size: 10pt; background: #f9f9f9; padding-top: 5px; padding-bottom: 5px; }
        img { max-width: 100%; height: auto; display: block; margin: 20px auto; border: 1px solid #eee; }
    ''')
    
    # Write PDF
    HTML(string=html_content, base_url=str(BASE)).write_pdf(PDF_FILE, stylesheets=[css])
    print(f"✓ Full Elite Manuscript PDF generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_full_pdf()
