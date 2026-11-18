#!/usr/bin/env python3
"""
=============================================================================
GENERATE STANDALONE TABLES REPORT
Delhi-NCR Circular Plastic Assessment
=============================================================================
Compiles 9-10 comprehensive empirical tables into a single Markdown/PDF.
=============================================================================
"""

import pandas as pd
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
MD_FILE = BASE / "Delhi_NCR_Empirical_Tables.md"
PDF_FILE = BASE / "Delhi_NCR_Empirical_Tables.pdf"

def df_to_markdown_table(df):
    """Converts a pandas dataframe to a markdown table string."""
    headers = " | ".join([str(c) for c in df.columns])
    separator = " | ".join(["---"] * len(df.columns))
    rows = []
    for _, row in df.iterrows():
        rows.append(" | ".join([str(x) for x in row.values]))
    
    return f"| {headers} |\n| {separator} |\n" + "\n".join([f"| {row} |" for row in rows])

def generate_tables():
    print("Compiling ALL empirical tables...")
    
    content = "# Empirical Evidence Tables: Delhi-NCR Circular Plastic Waste\n\n"
    content += "This document compiles all cross-layer empirical findings into a standalone tables annex for manuscript inclusion.\n\n"

    # ---------------------------------------------------------
    # Table 1: Robustness Summary
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(BASE / 'phase7d_convergence_summary.csv')
        df.columns = ['Methodological Test Category', 'Scenarios Evaluated', 'Mean Spearman (ρ)', 'Top-10 Overlap (%)', 'Robustness Interpretation']
        content += "## Table 1: Methodological Robustness & Sensitivity Convergence\n"
        content += "> Evaluates the stability of spatial priorities across 72 simulated methodological variations (e.g., Leave-One-Out, Index Weighting).\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 2: External Benchmarking
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7f_external_validation_benchmarks.csv')
        df.columns = ['Metric', 'Our Local Mean (%)', 'Standard Benchmark Range (%)', 'Status', 'Divergence (pp)', 'Empirical Interpretation']
        content += "## Table 2: Scientific Validation & Extracted Novelty\n"
        content += "> Benchmarks the Delhi dataset against standard Indian metro averages to mathematically extract localized novelty.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 3: Spatial Inequality
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7i_spatial_inequality_gini.csv')
        df.columns = ['Waste Variable', 'Gini Coefficient', 'Interpretation of Distribution']
        content += "## Table 3: Spatial Inequality Index (Gini)\n"
        content += "> Proves that toxicity (PVC) is hyper-concentrated in dense pockets, rather than distributed evenly across the urban environment.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 4: Spatial Autocorrelation
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7e_spatial_clustering_morans_i.csv')
        df['Morans_I'] = df['Morans_I'].round(4)
        df['Expected_I'] = df['Expected_I'].round(4)
        df.columns = ['Waste Variable', "Moran's I (Observed)", "Moran's I (Expected)", 'Spatial Clustering Status']
        content += "## Table 4: Spatial Autocorrelation & Neighborhood Dynamics\n"
        content += "> Assesses whether pollution characteristics follow smooth geographical gradients or exist as idiosyncratic hotspots.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 5: Spatial Context ANOVA
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7e_spatial_association_context.csv')
        df.columns = ['Target Metric', 'Context Factor (Predictor)', 'Kruskal-Wallis H', 'P-Value', 'Statistical Significance']
        content += "## Table 5: Non-Parametric ANOVA by Land Use and Income Level\n"
        content += "> Determines if localized pollution characteristics are systematically driven by demographic or zoning factors.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 6: Burden vs Composition Paradox
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7g_burden_vs_composition_correlation.csv')
        df.columns = ['Polymer Type', 'Spearman Correlation (ρ) vs Total Burden', 'P-Value', 'Significance', 'Empirical Finding']
        content += "## Table 6: The Burden-Composition Paradox Matrix\n"
        content += "> Evaluates the negative relationship between the total volume of plastic generated and its structural recyclability.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 7: Tonnage Extrapolation
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7i_tonnage_extrapolation.csv')
        df.columns = ['Waste Category', 'Estimated Physical Load (TPD)', 'Context & Basis']
        content += "## Table 7: City-Scale Tonnage Extrapolations\n"
        content += "> Translates empirical compositional percentages into actual daily tonnage processed by Delhi's municipal infrastructure.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 8: Facility Catchment Pressure
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7e_wte_catchment_profiles.csv')
        df.columns = ['WTE Facility (Catchment Hub)', 'Number of Localities Serviced', 'Mean Plastic Burden in Catchment (%)', 'Mean PVC (%)', 'Mean Distance to Facility (km)']
        content += "## Table 8: Waste Catchment Pressure on Infrastructure\n"
        content += "> Maps the spatial gravity of waste generation against the nearest infrastructure capacity.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 9: Policy Prioritization (EPR Treatability)
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7h_intervention_prioritization.csv').head(7)
        df['policy_priority_index'] = df['policy_priority_index'].round(2)
        df.columns = ['Locality Target', 'Land Use Profile', 'Plastic Burden (%)', 'PVC Toxicity (%)', 'Treatability Score (1-3)', 'Integrated Priority Index']
        content += "## Table 9: Policy Prioritization for EPR Enforcement (High Treatability Matrix)\n"
        content += "> Ranks target localities by integrating pollution gravity with enforcement viability (institutional/commercial zones).\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # ---------------------------------------------------------
    # Table 10: Logistics Routing
    # ---------------------------------------------------------
    try:
        df = pd.read_csv(OUT / '7h_bawana_diversion_routing.csv').head(5)
        df['extra_km_cost'] = df['extra_km_cost'].round(2)
        df.columns = ['Locality Re-Routed', 'Administrative Zone', 'Plastic Burden Diverted (%)', 'Original Distance to Bawana (km)', 'Alternative Under-Utilized Facility', 'Net Logistics Cost (+km)']
        content += "## Table 10: Infrastructure Relief via Diversion Scenario Simulation\n"
        content += "> Simulates the logistical cost of shifting high-burden waste from the over-stressed Bawana facility to under-utilized plants.\n\n"
        content += df_to_markdown_table(df) + "\n\n"
    except Exception as e: print(e)

    # Write Markdown
    with open(MD_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Markdown Tables created: {MD_FILE}")

    # Convert to PDF
    html_body = markdown.markdown(content, extensions=['extra', 'tables'])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Delhi-NCR Empirical Tables</title>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    css = CSS(string='''
        @page { size: A4 landscape; margin: 1.5cm; }
        body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 10pt; line-height: 1.4; color: #333; }
        h1 { font-size: 16pt; color: #2C3E50; text-align: center; margin-bottom: 20px; }
        h2 { font-size: 12pt; color: #34495E; border-bottom: 1px solid #eee; padding-bottom: 3px; margin-top: 25px; page-break-after: avoid; }
        blockquote { margin-left: 0; padding-left: 10px; border-left: 3px solid #3498DB; color: #555; font-style: italic; font-size: 9pt; margin-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 9pt; }
        th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
        th { background-color: #2C3E50; color: white; font-weight: bold; }
        tr:nth-child(even) { background-color: #F8F9F9; }
    ''')
    
    HTML(string=html_content).write_pdf(str(PDF_FILE), stylesheets=[css])
    print(f"✓ PDF Tables generated: {PDF_FILE}")

if __name__ == "__main__":
    generate_tables()
