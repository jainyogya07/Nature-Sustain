#!/usr/bin/env python3
"""
=============================================================================
MODULE 6: GENERATE MANUSCRIPT PDF TABLES
Delhi-NCR Circular Plastic Assessment
=============================================================================
Reads the final analytical outputs and generates a high-quality PDF 
ready for manuscript inclusion, summarizing the novel findings.
=============================================================================
"""

import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
OUTPUT_PDF = BASE / "Delhi_NCR_Circular_Plastic_Manuscript_Tables.pdf"

def df_to_table(df, col_widths=None):
    # Convert DataFrame to a list of lists for ReportLab
    data = [df.columns.tolist()] + df.values.tolist()
    
    # Create Table
    t = Table(data, colWidths=col_widths)
    
    # Add Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8F9F9")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#F8F9F9"), colors.HexColor("#EAEDED")])
    ])
    t.setStyle(style)
    return t

def generate_pdf():
    doc = SimpleDocTemplate(str(OUTPUT_PDF), pagesize=landscape(letter),
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor("#2C3E50"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor("#34495E"),
        spaceAfter=10,
        spaceBefore=15
    )
    
    desc_style = ParagraphStyle(
        'DescStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        textColor=colors.HexColor("#7F8C8D"),
        spaceAfter=15
    )

    elements = []
    
    # TITLE
    elements.append(Paragraph("Delhi-NCR Circular Plastic Waste: Empirical Policy Evidence", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", desc_style))
    elements.append(Spacer(1, 20))
    
    # -------------------------------------------------------------------------
    # 1. SPATIAL PRIORITIZATION MATRIX
    # -------------------------------------------------------------------------
    try:
        df_spatial = pd.read_csv(BASE / 'phase7e_spatial_prioritization_matrix.csv')
        df_spatial['pvc_percent_of_plastic'] = df_spatial['pvc_percent_of_plastic'].apply(lambda x: f"{x:.2f}%")
        df_spatial['plastic_burden_score'] = df_spatial['plastic_burden_score'].apply(lambda x: f"{x:.1f}")
        df_spatial = df_spatial[['spatial_priority_rank', 'locality', 'zone', 'plastic_burden_score', 'pvc_percent_of_plastic', 'intervention_recommendation']]
        df_spatial.columns = ['Rank', 'Locality', 'Zone', 'Burden Score (0-100)', 'PVC %', 'Policy Intervention Protocol']
        
        elements.append(Paragraph("Table 1: Integrated Spatial Prioritization Matrix (Robust Priorities)", subtitle_style))
        elements.append(Paragraph("Identifies the highly robust, spatially clustered priorities for targeted EPR and intervention based on multi-dimensional vulnerability.", desc_style))
        elements.append(df_to_table(df_spatial, col_widths=[40, 120, 90, 110, 60, 310]))
        elements.append(Spacer(1, 25))
    except Exception as e:
        print(f"Error loading spatial matrix: {e}")

    # -------------------------------------------------------------------------
    # 2. FACILITY UTILIZATION
    # -------------------------------------------------------------------------
    try:
        df_fac = pd.read_csv(BASE / 'phase7c_facility_utilization_classifications.csv')
        df_fac = df_fac[df_fac['facility'].isin(['Okhla', 'Ghazipur', 'Bawana', 'Tehkhand'])]
        df_fac = df_fac[['facility', 'capacity_tpd_msw', 'processing_tpd_msw', 'utilization_percent', 'classification', 'policy_recommendation']]
        df_fac.columns = ['WTE Facility', 'Design Capacity (TPD)', 'Actual Processing (TPD)', 'Utilization (%)', 'Status', 'Recommendation']
        df_fac['Utilization (%)'] = df_fac['Utilization (%)'].apply(lambda x: f"{x:.1f}%")
        
        elements.append(Paragraph("Table 2: Facility Heterogeneity and Capacity Utilization", subtitle_style))
        elements.append(Paragraph("Highlights the systemic imbalance in infrastructure utilization, quantifying headroom to the 85% optimal efficiency target.", desc_style))
        elements.append(df_to_table(df_fac, col_widths=[90, 120, 120, 90, 90, 220]))
        elements.append(Spacer(1, 25))
    except Exception as e:
        print(f"Error loading facility classification: {e}")

    # -------------------------------------------------------------------------
    # 3. OPTIMIZATION SCENARIOS
    # -------------------------------------------------------------------------
    try:
        df_opt = pd.read_csv(BASE / 'phase7c_wte_optimization_scenarios.csv')
        df_opt.columns = ['Scenario', 'Action', 'Capacity Impact', 'Cost Implication', 'Implementation Complexity']
        
        elements.append(Paragraph("Table 3: Infrastructure Optimization Scenarios", subtitle_style))
        elements.append(Paragraph("Policy pathways to address the 688.4 TPD optimal headroom without building new high-cost capacity.", desc_style))
        elements.append(df_to_table(df_opt, col_widths=[120, 220, 110, 140, 140]))
        elements.append(Spacer(1, 25))
    except Exception as e:
        print(f"Error loading optimization scenarios: {e}")
        
    elements.append(PageBreak())

    # -------------------------------------------------------------------------
    # 4. CITY PERFORMANCE INDICATOR
    # -------------------------------------------------------------------------
    try:
        df_city = pd.read_csv(BASE / 'phase7c_city_performance_indicator.csv')
        df_city['value'] = df_city.apply(lambda row: f"{row['value']:.2f}%" if row['unit'] == 'percent' else (f"{row['value']:.2f} pp" if row['unit'] == 'percentage_points' else f"{row['value']:.2f}"), axis=1)
        df_city = df_city[['metric', 'value', 'interpretation']]
        df_city.columns = ['Metric', 'Value', 'Interpretation']
        
        elements.append(Paragraph("Table 4: City-Level Plastic Processing Efficiency", subtitle_style))
        elements.append(Paragraph("Aggregate performance metrics based on official regulatory submissions.", desc_style))
        elements.append(df_to_table(df_city, col_widths=[140, 120, 120, 180]))
        elements.append(Spacer(1, 25))
    except Exception as e:
        print(f"Error loading city performance: {e}")

    # -------------------------------------------------------------------------
    # 5. ROBUSTNESS SUMMARY
    # -------------------------------------------------------------------------
    try:
        df_rob = pd.read_csv(BASE / 'phase7d_convergence_summary.csv')
        df_rob.columns = ['Test Category', 'Scenarios Evaluated', 'Mean Spearman Correlation (ρ)', 'Top-10 Overlap (%)', 'Interpretation']
        df_rob['Mean Spearman Correlation (ρ)'] = df_rob['Mean Spearman Correlation (ρ)'].apply(lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A")
        df_rob['Top-10 Overlap (%)'] = df_rob['Top-10 Overlap (%)'].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "N/A")
        
        elements.append(Paragraph("Table 5: Methodological Robustness and Sensitivity Convergence", subtitle_style))
        elements.append(Paragraph("Results of 72 sensitivity scenarios confirming the stability of the empirical findings (Moderate Overall Robustness).", desc_style))
        elements.append(df_to_table(df_rob, col_widths=[140, 120, 160, 120, 120]))
        elements.append(Spacer(1, 25))
    except Exception as e:
        print(f"Error loading robustness summary: {e}")
        
    # Build PDF
    doc.build(elements)
    print(f"✓ Successfully generated PDF: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_pdf()
