#!/usr/bin/env python3
"""
=============================================================================
PHASE 7G: INTEGRATED EMPIRICAL ANALYSIS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Cross-layer analytics correlating burden, composition, and infrastructure.
=============================================================================
"""

import pandas as pd
from scipy.stats import spearmanr
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
OUT.mkdir(parents=True, exist_ok=True)

def execute_integrated_analysis():
    print("=" * 70)
    print("PHASE 7G: INTEGRATED EMPIRICAL ANALYSIS")
    print("=" * 70)
    
    # Load core data
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df.fillna(0, inplace=True)
    
    # Load infrastructure proximity (from 7E)
    try:
        df_prox = pd.read_csv(OUT / '7e_infrastructure_proximity.csv')
        df_merged = df.merge(df_prox[['locality', 'nearest_wte_facility', 'distance_to_nearest_wte_km']], 
                             left_on='location', right_on='locality', how='left')
    except:
        print("Warning: 7E Proximity data not found, skipping infrastructure integration.")
        df_merged = df
        
    # -------------------------------------------------------------------------
    # 1. BURDEN × COMPOSITION (Spearman Correlation)
    # -------------------------------------------------------------------------
    print("\n1. Analyzing Burden × Composition Dynamics...")
    
    comp_cols = ['pet_percent_of_plastic', 'hdpe_ldpe_percent_of_plastic', 
                 'pvc_percent_of_plastic', 'pp_percent_of_plastic', 'ps_percent_of_plastic']
                 
    correlations = []
    burden_col = 'plastic_percent'
    
    for col in comp_cols:
        rho, p = spearmanr(df_merged[burden_col], df_merged[col])
        sig = "Significant (p<0.05)" if p < 0.05 else "Not Significant"
        
        correlations.append({
            'Resin_Type': col.replace('_percent_of_plastic', '').upper(),
            'Spearman_Rho': round(rho, 3),
            'p_value': round(p, 4),
            'Significance': sig,
            'Interpretation': f"Higher burden correlates with {'higher' if rho>0 else 'lower'} {col.split('_')[0].upper()}" if p<0.05 else "No robust correlation"
        })
        
    df_corr = pd.DataFrame(correlations)
    df_corr.to_csv(OUT / '7g_burden_vs_composition_correlation.csv', index=False)
    print(df_corr.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # 2. CROSS-LAYER CORRELATION MATRIX
    # -------------------------------------------------------------------------
    print("\n2. Generating Full Cross-Layer Correlation Matrix...")
    
    cols_of_interest = [
        'plastic_percent', 'pet_percent_of_plastic', 'hdpe_ldpe_percent_of_plastic', 
        'pvc_percent_of_plastic', 'pp_percent_of_plastic', 'ps_percent_of_plastic',
        'distance_to_nearest_wte_km'
    ]
    
    # Filter to existing columns
    cols_exist = [c for c in cols_of_interest if c in df_merged.columns]
    
    matrix = df_merged[cols_exist].corr(method='spearman').round(3)
    matrix.to_csv(OUT / '7g_cross_layer_correlation_matrix.csv')
    print("✓ Full correlation matrix saved to 7g_cross_layer_correlation_matrix.csv")
    
    # -------------------------------------------------------------------------
    # 3. FACILITY UTILIZATION × SPATIAL PRIORITIES
    # -------------------------------------------------------------------------
    print("\n3. Analyzing Facility Utilization × Spatial Priorities...")
    
    if 'nearest_wte_facility' in df_merged.columns:
        # Load utilization data from 7C
        try:
            util = pd.read_csv(BASE / 'phase7c_facility_utilization_classifications.csv')
            util_dict = dict(zip(util['facility'], util['utilization_percent']))
            class_dict = dict(zip(util['facility'], util['classification']))
            
            # Map utilization to catchment areas
            fac_summary = df_merged.groupby('nearest_wte_facility').agg(
                mean_burden=('plastic_percent', 'mean'),
                high_burden_localities=('plastic_percent', lambda x: (x > 15.0).sum()),
                high_pvc_localities=('pvc_percent_of_plastic', lambda x: (x > 5.0).sum())
            ).reset_index()
            
            fac_summary['utilization_percent'] = fac_summary['nearest_wte_facility'].map(util_dict)
            fac_summary['facility_status'] = fac_summary['nearest_wte_facility'].map(class_dict)
            
            # Sort by burden
            fac_summary = fac_summary.sort_values('mean_burden', ascending=False)
            fac_summary.to_csv(OUT / '7g_facility_spatial_pressure.csv', index=False)
            
            print(fac_summary[['nearest_wte_facility', 'utilization_percent', 'facility_status', 'mean_burden', 'high_burden_localities']].to_string(index=False))
            
            print("\nKey Insight (Infrastructure Routing):")
            bawana_burden = fac_summary.loc[fac_summary['nearest_wte_facility'] == 'Bawana', 'mean_burden'].values[0] if 'Bawana' in fac_summary['nearest_wte_facility'].values else 0
            ghazipur_burden = fac_summary.loc[fac_summary['nearest_wte_facility'] == 'Ghazipur', 'mean_burden'].values[0] if 'Ghazipur' in fac_summary['nearest_wte_facility'].values else 0
            
            print(f"The over-stressed facility (Bawana) handles localities with a mean burden of {bawana_burden:.1f}%.")
            print(f"The under-utilized facility (Ghazipur) handles localities with a mean burden of {ghazipur_burden:.1f}%.")
            
        except Exception as e:
            print(f"Could not link utilization data: {e}")
            
    print("\n✓ Phase 7G Integrated Empirical Analysis Complete.")

if __name__ == "__main__":
    execute_integrated_analysis()
