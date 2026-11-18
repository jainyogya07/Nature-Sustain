#!/usr/bin/env python3
"""
=============================================================================
PHASE 8E & 8F: ELITE POLICY-MODEL SENSITIVITY VALIDATION
Delhi-NCR Circular Plastic Assessment
=============================================================================
1. EPR Priority Score Sensitivity Analysis (Multi-Weighting Survival)
2. Tonnage Extrapolation Confidence Intervals (±10% Baseline)
=============================================================================
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
OUT.mkdir(parents=True, exist_ok=True)

def execute_elite_policy_sensitivity():
    print("=" * 70)
    print("PHASE 8E/8F: ELITE POLICY-MODEL SENSITIVITY")
    print("=" * 70)
    
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df.fillna(0, inplace=True)
    
    # -------------------------------------------------------------------------
    # 1. EPR Priority Score Sensitivity (Multi-Weighting)
    # -------------------------------------------------------------------------
    print("\n1. Running EPR Priority Matrix Sensitivity...")
    
    def score_treatability(land_use):
        lu = str(land_use).lower()
        if 'commercial' in lu or 'institutional' in lu: return 3
        elif 'public' in lu or 'tourist' in lu or 'mixed' in lu: return 2
        else: return 1
            
    df['treatability_score'] = df['land_use_type'].apply(score_treatability)
    
    burden_max = df['plastic_percent'].max()
    pvc_max = df['pvc_percent_of_plastic'].max()
    df['norm_burden'] = df['plastic_percent'] / (burden_max if burden_max > 0 else 1)
    df['norm_pvc'] = df['pvc_percent_of_plastic'] / (pvc_max if pvc_max > 0 else 1)
    
    # Scenario A: Equal Weights (Base)
    # Priority = (Burden * 0.5 + PVC * 0.5) * Treatability
    df['priority_A_equal'] = (df['norm_burden'] * 0.5 + df['norm_pvc'] * 0.5) * df['treatability_score']
    
    # Scenario B: Burden Heavy
    df['priority_B_burden'] = (df['norm_burden'] * 0.8 + df['norm_pvc'] * 0.2) * df['treatability_score']
    
    # Scenario C: PVC Heavy
    df['priority_C_pvc'] = (df['norm_burden'] * 0.2 + df['norm_pvc'] * 0.8) * df['treatability_score']
    
    # Scenario D: Treatability Driven (Squared Treatability)
    df['priority_D_treat'] = (df['norm_burden'] * 0.5 + df['norm_pvc'] * 0.5) * (df['treatability_score'] ** 2)
    
    ranks = pd.DataFrame({'location': df['location']})
    ranks['Rank_A'] = df['priority_A_equal'].rank(ascending=False)
    ranks['Rank_B'] = df['priority_B_burden'].rank(ascending=False)
    ranks['Rank_C'] = df['priority_C_pvc'].rank(ascending=False)
    ranks['Rank_D'] = df['priority_D_treat'].rank(ascending=False)
    
    # Calculate Mean Rank and Standard Deviation of Rank (Sensitivity)
    ranks['Mean_Rank'] = ranks[['Rank_A', 'Rank_B', 'Rank_C', 'Rank_D']].mean(axis=1)
    ranks['Rank_SD'] = ranks[['Rank_A', 'Rank_B', 'Rank_C', 'Rank_D']].std(axis=1)
    
    elite_priorities = ranks.sort_values('Mean_Rank').head(10)
    
    out_priorities = df.merge(elite_priorities[['location', 'Mean_Rank', 'Rank_SD']], on='location', how='right')
    out_priorities = out_priorities[['location', 'land_use_type', 'plastic_percent', 'pvc_percent_of_plastic', 'Mean_Rank', 'Rank_SD']].sort_values('Mean_Rank')
    
    out_priorities.to_csv(OUT / '8e_epr_priority_sensitivity_elite.csv', index=False)
    print("EPR Target Stability across 4 subjective weighting paradigms:")
    print(out_priorities.head(5).to_string(index=False))
    
    # -------------------------------------------------------------------------
    # 2. Tonnage Extrapolation Confidence Intervals
    # -------------------------------------------------------------------------
    print("\n2. Running Tonnage Extrapolation Sensitivity (±10% Baseline)...")
    
    BASE_MSW_TPD = 11328.0
    msw_bounds = [BASE_MSW_TPD * 0.9, BASE_MSW_TPD, BASE_MSW_TPD * 1.1] # -10%, Base, +10%
    
    mean_plastic_pct = df['plastic_percent'].mean()
    mean_pvc_pct_of_plastic = df['pvc_percent_of_plastic'].mean()
    mean_hdpe_ldpe_pct = df['hdpe_ldpe_percent_of_plastic'].mean()
    
    tonnage_sensitivity = []
    
    for msw in msw_bounds:
        tot_plas = msw * (mean_plastic_pct / 100.0)
        hdpe = tot_plas * (mean_hdpe_ldpe_pct / 100.0)
        pvc = tot_plas * (mean_pvc_pct_of_plastic / 100.0)
        
        tonnage_sensitivity.append({
            'Scenario': f"MSW = {int(msw)} TPD",
            'Total_Plastic_TPD': round(tot_plas, 1),
            'Recyclable_HDPE_TPD': round(hdpe, 1),
            'Toxic_PVC_TPD': round(pvc, 1)
        })
        
    df_tonnage = pd.DataFrame(tonnage_sensitivity)
    df_tonnage.to_csv(OUT / '8f_tonnage_extrapolation_bounds_elite.csv', index=False)
    print(df_tonnage.to_string(index=False))
    
    print("\n✓ Phase 8E/8F Complete.")

if __name__ == "__main__":
    execute_elite_policy_sensitivity()
