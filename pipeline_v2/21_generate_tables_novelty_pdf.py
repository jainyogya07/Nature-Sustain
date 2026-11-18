#!/usr/bin/env python3
"""
=============================================================================
PHASE 8: TABLES & NOVELTY PDF GENERATOR
Delhi-NCR Circular Plastic Assessment
=============================================================================
Creates a standalone PDF containing only the context/abstract, 
the final novelty impact statement, and the 6 elite tables.
=============================================================================
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TABLES_FILE = BASE / "Delhi_NCT_Elite_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCT_Tables_and_Novelty_Impact.pdf"

def generate_custom_pdf():
    print("Compiling Tables + Novelty Impact PDF...")
    
    # 1. Add Context & Novelty Impact
    intro_content = """# Observational Heterogeneity in Urban Plastic Waste: Context, Tables, and Novelty Impact

**Note on Methodological Scope:** N=58 represents the full locality-level observational dataset. N=55 represents the subset of complete cases for detailed resin-level compositional analyses. The three localities excluded from resin-level analyses were excluded because of incomplete compositional observations. The spatial and infrastructure footprint is strictly defined as Delhi NCT.

## 1. Study Context
Urban solid waste management traditionally relies on macro-level averages, which may obscure critical micro-spatial heterogeneity. This observational study of Delhi NCT (N=58 localities) investigates the spatial, socioeconomic, and infrastructural dimensions of plastic waste generation. While the city-wide average plastic burden (10.82%) exhibits concordance with standard national baselines, this aggregate metric masks statistically significant associations between plastic fraction and local socioeconomic status (Kruskal-Wallis FDR p=0.0116) as well as land-use classification (FDR p=0.0223). Global spatial autocorrelation was non-significant (p=0.247), indicating that pollution does not follow smooth geographical gradients. However, Local Moran's I analysis (LISA) identified isolated, statistically significant micro-spatial hotspots.

## 2. Policy Scenarios and Novelty Impact
Unlike traditional macro-level solid waste assessments, this study demonstrates that plastic burden exhibits statistically significant micro-spatial associations with socioeconomic and land-use contexts. 

By mapping this heterogeneity onto the existing Waste-to-Energy infrastructure network, we identified specific, actionable intervention opportunities. Under a hypothetical operational scenario assuming optimal 9-tonne payloads and flat ₹50/km round-trip transport costs, diverting specific high-burden localities away from the over-stressed Bawana facility toward under-utilized alternatives yields theoretical diversion costs ranging from ₹13 to ₹40/tonne. These values represent transport-cost scenarios under fixed routing and payload assumptions and should not be interpreted as realized municipal operating costs or profitability estimates. However, the core policy implication indicates that municipalities could evaluate a shift from uniform city-wide EPR quotas toward localized, precision-targeted logistics interventions.

---

"""
    
    # 2. Read Tables
    with open(TABLES_FILE, 'r', encoding='utf-8') as f:
        tables_content = f.read()
        
    # Replace the duplicate main header from the tables file to make it flow better
    tables_content = tables_content.replace("# Elite Empirical Evidence Tables: Delhi NCT Circular Plastic Waste\n\n", "## 3. Elite Empirical Evidence Tables\n\n")
    
    # 4. Combine all
    full_markdown = intro_content + tables_content
    
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
    ''')
    
    # Write PDF
    HTML(string=html_content, base_url=str(BASE)).write_pdf(PDF_FILE, stylesheets=[css])
    print(f"✓ Custom Tables + Novelty PDF generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_custom_pdf()
