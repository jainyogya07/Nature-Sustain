#!/usr/bin/env python3
"""
=============================================================================
PHASE 8H: ELITE VISUAL FIGURES
Delhi-NCR Circular Plastic Assessment
=============================================================================
Generates 3 publication-ready visual figures supporting the final 
empirical narrative synthesis (13+ IF quality).
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE = Path(__file__).resolve().parents[1]
IN = BASE / "pipeline_v2" / "advanced_analytics"
OUT = BASE / "pipeline_v2" / "visual_assets"
OUT.mkdir(parents=True, exist_ok=True)

# Academic styling
plt.style.use('seaborn-v0_8-paper')
sns.set_theme(style="ticks", font="serif")
sns.set_context("paper", font_scale=1.2)

def generate_visuals():
    print("=" * 70)
    print("PHASE 8H: GENERATING ELITE VISUAL FIGURES")
    print("=" * 70)

    df_main = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df_epr = pd.read_csv(IN / '8e_epr_priority_stability_elite.csv')
    df_div = pd.read_csv(IN / '8e_economic_diversion_cost_elite.csv')

    # ---------------------------------------------------------
    # Figure 1: Socio-Spatial Context (Boxplots)
    # ---------------------------------------------------------
    print("Generating Figure 1: Socio-Spatial Inequality...")
    df_plot1 = df_main.dropna(subset=['income_level', 'plastic_percent', 'land_use_type']).copy()
    
    # Sort categories for consistency
    income_order = sorted(df_plot1['income_level'].unique())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    sns.boxplot(data=df_plot1, x='income_level', y='plastic_percent', order=income_order, ax=ax1, palette='Blues_d', width=0.5)
    sns.swarmplot(data=df_plot1, x='income_level', y='plastic_percent', order=income_order, ax=ax1, color=".25", alpha=0.7, size=4)
    ax1.set_title(r'Plastic Burden by Socio-Economic Tier\n(Kruskal-Wallis FDR p=0.0116, $\epsilon^2$=0.208)', fontweight='bold')
    ax1.set_ylabel('Plastic Burden (%)')
    ax1.set_xlabel('Income Level')
    
    sns.boxplot(data=df_plot1, x='land_use_type', y='plastic_percent', ax=ax2, palette='Greens_d', width=0.5)
    sns.swarmplot(data=df_plot1, x='land_use_type', y='plastic_percent', ax=ax2, color=".25", alpha=0.7, size=4)
    ax2.set_title(r'Plastic Burden by Urban Land Use\n(Kruskal-Wallis FDR p=0.0223, $\epsilon^2$=0.193)', fontweight='bold')
    ax2.set_ylabel('')
    ax2.set_xlabel('Land Use Type')
    plt.xticks(rotation=45, ha='right')
    
    sns.despine()
    plt.tight_layout()
    fig1_path = OUT / 'Fig1_SocioSpatial_Inequality.png'
    plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # Figure 2: Intervention Priority Stability (Bar Chart)
    # ---------------------------------------------------------
    print("Generating Figure 2: Priority Stability...")
    df_plot2 = df_epr.head(10).copy()
    df_plot2 = df_plot2.sort_values('Mean_Rank')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Color coding based on stability status
    colors = ['#2ca02c' if 'Stable' in s else '#d62728' for s in df_plot2['Stability_Status']]
    
    bars = ax.bar(df_plot2['location'], df_plot2['Mean_Rank'], yerr=df_plot2['Rank_SD'], capsize=5, color=colors, alpha=0.8, edgecolor='black')
    
    ax.set_title('EPR Intervention Priority Stability Under Alternative Weighting Paradigms', fontweight='bold', pad=20)
    ax.set_ylabel('Mean Priority Rank\n(Lower = Higher Priority)')
    ax.set_xlabel('Candidate Target Locality')
    plt.xticks(rotation=45, ha='right')
    
    # Custom legend
    import matplotlib.patches as mpatches
    stable_patch = mpatches.Patch(color='#2ca02c', label='Highly Stable (SD < 2.0)')
    sensitive_patch = mpatches.Patch(color='#d62728', label='Method-Sensitive (SD > 4.0)')
    plt.legend(handles=[stable_patch, sensitive_patch], loc='upper left')
    
    sns.despine()
    plt.tight_layout()
    fig2_path = OUT / 'Fig2_Intervention_Stability.png'
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # Figure 3: Infrastructure Scenario Economics (Scatter)
    # ---------------------------------------------------------
    print("Generating Figure 3: Economic Diversion Scenario...")
    df_plot3 = df_div.copy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(df_plot3['financial_cost_inr_per_tonne'], df_plot3['plastic_percent'], 
                         c=df_plot3['extra_km_cost'], cmap='viridis', s=100, alpha=0.8, edgecolor='black')
    
    # Add colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Additional Round-Trip Distance (Δ km)')
    
    # Annotate top 5 most efficient targets
    top_efficient = df_plot3.sort_values('financial_cost_inr_per_tonne').head(5)
    for idx, row in top_efficient.iterrows():
        ax.annotate(row['location'], (row['financial_cost_inr_per_tonne'], row['plastic_percent']),
                    xytext=(5, 5), textcoords='offset points', fontsize=9, 
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    ax.set_title('Logistics Economics of Waste Diversion to Under-Utilized Infrastructure', fontweight='bold', pad=20)
    ax.set_xlabel('Operational Logistics Cost (₹/tonne, round-trip assumed)')
    ax.set_ylabel('Divertable Plastic Burden (%)')
    
    # Add quadrant lines (median cost, median burden)
    ax.axhline(df_plot3['plastic_percent'].median(), color='gray', linestyle='--', alpha=0.5)
    ax.axvline(df_plot3['financial_cost_inr_per_tonne'].median(), color='gray', linestyle='--', alpha=0.5)
    
    # Quadrant text
    ax.text(df_plot3['financial_cost_inr_per_tonne'].min(), df_plot3['plastic_percent'].max(), 'High Yield / Low Cost', 
            fontsize=10, style='italic', color='green', alpha=0.8, va='top')
    
    sns.despine()
    plt.tight_layout()
    fig3_path = OUT / 'Fig3_Economic_Diversion.png'
    plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n✓ 3 Elite Visual Figures successfully generated and saved to: {OUT}")

if __name__ == "__main__":
    generate_visuals()
