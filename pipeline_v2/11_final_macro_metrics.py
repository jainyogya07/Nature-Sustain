#!/usr/bin/env python3
"""
=============================================================================
PHASE 7I: FINAL ADVANCED MACRO METRICS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Calculates:
1. Spatial Inequality Index (Gini Coefficient) for plastic burden.
2. Tonnage Extrapolation (translating percentages to actual MSW TPD).
=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
OUT.mkdir(parents=True, exist_ok=True)

# Delhi Official MSW Generation (from DPCC / MCD reports ~2023-2025)
TOTAL_MSW_TPD = 11328.0

def gini_coefficient(x):
    """Calculate the Gini coefficient of a numpy array."""
    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad / np.mean(x)
    # Gini coefficient is half the relative mean absolute difference
    return 0.5 * rmad

def execute_macro_metrics():
    print("=" * 70)
    print("PHASE 7I: FINAL ADVANCED MACRO METRICS")
    print("=" * 70)
    
    # Load core data
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df.fillna(0, inplace=True)
    
    # -------------------------------------------------------------------------
    # 1. SPATIAL INEQUALITY (Gini Index)
    # -------------------------------------------------------------------------
    print("\n1. Calculating Spatial Inequality...")
    
    burdens = df['plastic_percent'].values
    pvcs = df['pvc_percent_of_plastic'].values
    
    gini_burden = gini_coefficient(burdens)
    gini_pvc = gini_coefficient(pvcs)
    
    inequality = pd.DataFrame([
        {'Metric': 'Plastic Burden %', 'Gini_Coefficient': round(gini_burden, 3), 'Interpretation': 'Moderate spatial inequality' if gini_burden < 0.4 else 'High spatial inequality'},
        {'Metric': 'PVC % of Plastic', 'Gini_Coefficient': round(gini_pvc, 3), 'Interpretation': 'Moderate spatial inequality' if gini_pvc < 0.4 else 'High spatial inequality (Highly concentrated hotspots)'}
    ])
    
    inequality.to_csv(OUT / '7i_spatial_inequality_gini.csv', index=False)
    print(inequality.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # 2. TONNAGE EXTRAPOLATION
    # -------------------------------------------------------------------------
    print("\n2. Extrapolating Tonnage to City Scale...")
    print(f"Base Assumption: Delhi Total MSW Generation = {TOTAL_MSW_TPD:,.0f} TPD")
    
    mean_plastic_pct = df['plastic_percent'].mean()
    mean_pvc_pct_of_plastic = df['pvc_percent_of_plastic'].mean()
    mean_hdpe_ldpe_pct = df['hdpe_ldpe_percent_of_plastic'].mean()
    
    # Total Plastic TPD
    total_plastic_tpd = TOTAL_MSW_TPD * (mean_plastic_pct / 100.0)
    
    # Highly Recyclable TPD (HDPE/LDPE)
    recyclable_tpd = total_plastic_tpd * (mean_hdpe_ldpe_pct / 100.0)
    
    # Problematic/Toxic TPD (PVC)
    pvc_tpd = total_plastic_tpd * (mean_pvc_pct_of_plastic / 100.0)
    
    extrapolation = pd.DataFrame([
        {'Category': 'Total Municipal Solid Waste', 'Estimated_TPD': round(TOTAL_MSW_TPD, 1), 'Note': 'Official Delhi Baseline'},
        {'Category': 'Total Plastic Waste', 'Estimated_TPD': round(total_plastic_tpd, 1), 'Note': f'Based on {mean_plastic_pct:.1f}% mean burden'},
        {'Category': 'High-Value Recyclable Plastic (HDPE/LDPE)', 'Estimated_TPD': round(recyclable_tpd, 1), 'Note': f'Based on {mean_hdpe_ldpe_pct:.1f}% composition'},
        {'Category': 'Highly Toxic / Problematic Plastic (PVC)', 'Estimated_TPD': round(pvc_tpd, 1), 'Note': f'Based on {mean_pvc_pct_of_plastic:.1f}% composition'}
    ])
    
    extrapolation.to_csv(OUT / '7i_tonnage_extrapolation.csv', index=False)
    print("\nCity-Scale Tonnage Projections:")
    print(extrapolation.to_string(index=False))
    
    print("\n✓ Phase 7I Macro Metrics Complete.")

if __name__ == "__main__":
    execute_macro_metrics()
