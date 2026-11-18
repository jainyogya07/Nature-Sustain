#!/usr/bin/env python3
"""
=============================================================================
GENERATE ELITE TABLES REPORT
Delhi-NCR Circular Plastic Assessment
=============================================================================
Compiles the 6 condensed, rigorously validated Phase 8 empirical tables 
into a single PDF annex for manuscript inclusion.
=============================================================================
"""

import pandas as pd
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
MD_FILE = BASE / "Delhi_NCR_Elite_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCR_Elite_Empirical_Tables.pdf"

def df_to_markdown_table(df):
    headers = " | ".join([str(c) for c in df.columns])
    separator = " | ".join(["---"] * len(df.columns))
    rows = []
    for _, row in df.iterrows():
        rows.append(" | ".join([str(x) for x in row.values]))
    
    return f"| {headers} |\n| {separator} |\n" + "\n".join([f"| {row} |" for row in rows])

def generate_elite_tables():
    print("Compiling ELITE empirical tables...")
    
    content = "# Elite Empirical Evidence Tables: Delhi-NCR Circular Plastic Waste\n\n"
    content += "This document compiles the finalized, rigorously validated (FDR-corrected, permutation-tested, multi-weighted) empirical findings into a 6-table annex for high-impact journal inclusion.\n\n"

    # ---------------------------------------------------------
    # Table 1: External Benchmarking (Concordance)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7f_external_validation_benchmarks.csv')
        df = df[['Metric', 'Our_Mean', 'Benchmark_Range', 'Status']]
        df.columns = ['Plastic Metric', 'Delhi-NCR Dataset Mean (%)', 'Standardized Reference Baseline (%)', 'Baseline Concordance']
        content += "## Table 1: Baseline Concordance & Data Provenance\n"
        content += "> Benchmarks the dataset against standard CPCB (2020-21) and NEERI averages, demonstrating macro-level concordance that masks micro-spatial inequality.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 2: Spatial Association (ANOVA + FDR)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8b_spatial_association_elite.csv')
        df = df[['Metric', 'Context', 'H_Statistic', 'Epsilon_Sq (Effect Size)', 'FDR_Adjusted_P', 'Interpretation']]
        df.columns = ['Waste Variable', 'Socio-Spatial Context', 'Kruskal-Wallis H', 'Effect Size (ε²)', 'FDR-Adjusted P-Value', 'Statistical Conclusion']
        content += "## Table 2: Spatial Association (ANOVA with FDR Correction & Effect Sizes)\n"
        content += "> Applies non-parametric Kruskal-Wallis testing with Benjamini-Hochberg False Discovery Rate (FDR) adjustments to prove demographic associations with plastic burden.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 3: Spatial Clustering (Permutation)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8c_spatial_clustering_permutation.csv')
        df.columns = ['Waste Variable', "Observed Global Moran's I", "Expected Index", 'Permutation Pseudo P-Value']
        content += "## Table 3: Global Spatial Autocorrelation (Monte Carlo Permutation, n=999)\n"
        content += "> Confirms via permutation testing that pollution does not follow smooth geographical gradients, but rather exists as idiosyncratic, chaotic hotspots.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 4: Tonnage Sensitivity Bounds
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8f_tonnage_extrapolation_bounds_elite.csv')
        df.columns = ['MSW Generation Scenario', 'Total Plastic Projected (TPD)', 'Recyclable HDPE/LDPE Projected (TPD)', 'Toxic PVC Projected (TPD)']
        content += "## Table 4: City-Scale Tonnage Projections (Sensitivity Bounds)\n"
        content += "> Translates empirical compositional percentages into actual daily tonnage processed by Delhi's municipal infrastructure, bounded by a ±10% margin.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 5: EPR Policy Sensitivity
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '8e_epr_priority_sensitivity_elite.csv').head(5)
        df = df[['location', 'land_use_type', 'Mean_Rank', 'Rank_SD']]
        df.columns = ['Intervention Target (Locality)', 'Land Use Zone', 'Mean Priority Rank (Multi-Weighting)', 'Rank Volatility (SD)']
        content += "## Table 5: High-Impact Target Stability (Multi-Weighting Survival Analysis)\n"
        content += "> Subjects the EPR priority matrix to four extreme weighting paradigms to prove that top commercial/institutional targets survive regardless of subjective methodology.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 6: Diversion Scenario Simulation
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7h_bawana_diversion_routing.csv').head(4)
        df['extra_km_cost'] = df['extra_km_cost'].round(2)
        df = df[['location', 'plastic_percent', 'best_alternative', 'extra_km_cost']]
        df.columns = ['Candidate Locality for Diversion', 'Plastic Burden (%)', 'Target Under-Utilized Facility', 'Simulation Cost (Δ km)']
        content += "## Table 6: Infrastructure Relief via Diversion Scenario Simulation\n"
        content += "> Models a Haversine-based logistics scenario to calculate the minor physical transit cost required to shift high-burden waste away from over-stressed infrastructure.\n\n"
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
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f8f9fa; font-weight: bold; }
        tr:nth-child(even) { background-color: #fdfdfd; }
        blockquote { font-style: italic; color: #555; border-left: 4px solid #ccc; padding-left: 10px; margin: 15px 0; font-size: 10pt; }
    ''')
    
    HTML(string=html_content).write_pdf(PDF_FILE, stylesheets=[css])
    print(f"✓ PDF Tables generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_elite_tables()
