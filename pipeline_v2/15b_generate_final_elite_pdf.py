#!/usr/bin/env python3
"""
=============================================================================
GENERATE FINAL ELITE TABLES REPORT (PHASE 8H)
Delhi-NCR Circular Plastic Assessment
=============================================================================
Compiles the strictly validated 6 Phase 8 empirical tables into a PDF.
Implements rigorous scope (Delhi NCT), traceable benchmarking, LISA hotspots, 
and actual financial diversion modeling.
=============================================================================
"""

import pandas as pd
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
MD_FILE = BASE / "Delhi_NCT_Elite_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCT_Elite_Empirical_Tables.pdf"

def df_to_markdown_table(df):
    headers = " | ".join([str(c) for c in df.columns])
    separator = " | ".join(["---"] * len(df.columns))
    rows = []
    for _, row in df.iterrows():
        rows.append(" | ".join([str(x) for x in row.values]))
    
    return f"| {headers} |\n| {separator} |\n" + "\n".join([f"| {row} |" for row in rows])

def generate_elite_tables():
    print("Compiling FINAL ELITE empirical tables...")
    
    content = "# Elite Empirical Evidence Tables: Delhi NCT Circular Plastic Waste\n\n"
    content += "This document compiles the finalized, rigorously validated empirical findings into a 6-table annex for high-impact journal inclusion. Strict causal discipline, traceability, and spatial significance testing have been enforced.\n\n"
    content += "> *Methodological Scope Note: N=58 represents the full locality-level observational dataset. N=55 represents the subset of complete cases for detailed resin-level compositional analyses. The spatial and infrastructure footprint is strictly defined as Delhi NCT.*\n\n"

    # ---------------------------------------------------------
    # Table 1: Traceable Benchmarking
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8a_benchmark_provenance_elite.csv')
        df.columns = ['Plastic Metric', 'Delhi NCT Sample Mean (%)', 'Reference Baseline (%)', 'Year', 'Geography', 'Methodological Comparability', 'Source', 'Concordance']
        content += "## Table 1: Data Provenance & Baseline Concordance\n"
        content += "> Establishes rigorous comparability between the Delhi NCT sample (N=58) and standardized national/regional baselines.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 2: Spatial Association (Kruskal-Wallis)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8b_spatial_association_elite.csv')
        df = df[['Metric', 'Context', 'H_Statistic', 'Epsilon_Sq (Effect Size)', 'FDR_Adjusted_P', 'Interpretation']]
        df.columns = ['Waste Variable', 'Socio-Spatial Context', 'Kruskal-Wallis H', 'Effect Size (ε²)', 'FDR-Adjusted P-Value', 'Statistical Conclusion']
        content += "## Table 2: Spatial Association (Kruskal-Wallis Tests with FDR Correction and Effect Sizes)\n"
        content += "> Demonstrates a statistically significant association between demographic zones and plastic burden generation, robust to multiple-testing corrections.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 3: Spatial Clustering (LISA)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8c_lisa_hotspots_elite.csv').head(7)
        df.columns = ['Micro-Spatial Locality', 'Plastic Burden (%)', "Local Moran's I", 'LISA Pseudo P-Value', 'Spatial Cluster Classification']
        content += "## Table 3: Local Spatial Autocorrelation (LISA) Hotspot Detection\n"
        content += "> Identifies statistically significant localized spatial clusters (p < 0.05) and marginal/exploratory spatial patterns (0.05 ≤ p < 0.10) using 999 Monte Carlo permutations, demonstrating that high-burden areas exhibit chaotic, disjointed clustering rather than global geographical gradients.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 4: Tonnage Sensitivity Bounds (Delhi NCT)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8f_tonnage_extrapolation_bounds_elite.csv')
        df.columns = ['Delhi NCT MSW Generation Scenario', 'Total Plastic Projected (TPD)', 'Recyclable HDPE/LDPE Projected (TPD)', 'PVC-bearing fraction (TPD)']
        content += "## Table 4: Delhi NCT City-Scale Tonnage Projections (Sensitivity Bounds)\n"
        content += "> Translates empirical compositional percentages into scenario-based daily physical loads processed by Delhi NCT's municipal infrastructure, bounded by a ±10% margin.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 5: EPR Policy Stability
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8e_epr_priority_stability_elite.csv').head(6)
        df = df[['location', 'land_use_type', 'Mean_Rank', 'Rank_SD', 'Stability_Status']]
        df.columns = ['Intervention Target (Locality)', 'Land Use Zone', 'Mean Priority Rank', 'Rank Volatility (SD)', 'Stability Classification']
        content += "## Table 5: Intervention-Priority Stability under Alternative Weighting Schemes\n"
        content += "> Assesses intervention-priority stability under four alternative subjective weighting paradigms, distinguishing structurally stable targets from method-sensitive priorities.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 6: Economic Diversion Scenario
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8e_economic_diversion_cost_elite.csv').head(5)
        df = df[['location', 'best_alternative', 'extra_km_cost', 'financial_cost_inr_per_tonne']]
        df.columns = ['Candidate Locality for Diversion', 'Target Under-Utilized Facility', 'Additional Routing Distance (Δ km)', 'Logistics Cost (₹/tonne)']
        content += "## Table 6: Infrastructure Relief via Diversion Scenario Simulation\n"
        content += "> Calculates scenario-based transport logistics costs for shifting high-burden waste away from over-stressed infrastructure, assuming standard 9-tonne municipal capacity and ₹50/km transport costs. **Round-trip routing distance was assumed** to fully account for vehicle return logistics.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # Write to Markdown
    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Markdown Tables created: {MD_FILE}")

    # Convert to PDF
    html_content = markdown.markdown(content, extensions=['tables'])
    
    # CSS for academic styling
    css = CSS(string='''
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.4; }
        h1 { font-size: 18pt; text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; }
        h2 { font-size: 13pt; margin-top: 30px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 25px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 9.5pt; }
        th { background-color: #f8f9fa; font-weight: bold; }
        tr:nth-child(even) { background-color: #fdfdfd; }
        blockquote { font-style: italic; color: #555; border-left: 4px solid #ccc; padding-left: 10px; margin: 15px 0; font-size: 10pt; }
    ''')
    
    HTML(string=html_content).write_pdf(PDF_FILE, stylesheets=[css])
    print(f"✓ Final Elite PDF Tables generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_elite_tables()
