#!/usr/bin/env python3
"""
=============================================================================
PHASE 7H: ADVANCED POLICY & IMPACT ANALYSIS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Translates empirical data into actionable policy mechanisms:
1. Intervention Treatability Matrix
2. Infrastructure Routing Scenario Simulation
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
OUT.mkdir(parents=True, exist_ok=True)

def execute_policy_analysis():
    print("=" * 70)
    print("PHASE 7H: ADVANCED POLICY & IMPACT ANALYSIS")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df.fillna(0, inplace=True)
    
    try:
        df_prox = pd.read_csv(OUT / '7e_infrastructure_proximity.csv')
        df = df.merge(df_prox[['locality', 'nearest_wte_facility', 'distance_to_nearest_wte_km', 
                               'distance_to_okhla', 'distance_to_ghazipur', 'distance_to_bawana', 'distance_to_tehkhand']], 
                      left_on='location', right_on='locality', how='left')
    except:
        print("Error loading proximity data.")
        return

    # -------------------------------------------------------------------------
    # 1. INTERVENTION TREATABILITY MATRIX
    # -------------------------------------------------------------------------
    print("\n1. Calculating Intervention Treatability Matrix...")
    
    # Treatability Logic:
    # High (3): Commercial, Institutional (Easy to enforce EPR/Corporate compliance)
    # Medium (2): Public, Tourist, Mixed (Municipal enforcement possible)
    # Low (1): Residential, Slum (Requires behavioral change, harder to enforce)
    
    def score_treatability(land_use):
        lu = str(land_use).lower()
        if 'commercial' in lu or 'institutional' in lu:
            return 3
        elif 'public' in lu or 'tourist' in lu or 'mixed' in lu:
            return 2
        else:
            return 1
            
    df['treatability_score'] = df['land_use_type'].apply(score_treatability)
    
    # Priority Score = (Plastic Burden Normalized 0-1) * (PVC Normalized 0-1) * Treatability
    burden_max = df['plastic_percent'].max()
    pvc_max = df['pvc_percent_of_plastic'].max()
    
    df['norm_burden'] = df['plastic_percent'] / (burden_max if burden_max > 0 else 1)
    df['norm_pvc'] = df['pvc_percent_of_plastic'] / (pvc_max if pvc_max > 0 else 1)
    
    # Add a base weight to burden to ensure high burden areas are still prioritized even if PVC is 0
    df['policy_priority_index'] = (df['norm_burden'] * 0.7 + df['norm_pvc'] * 0.3) * df['treatability_score']
    
    priority = df.sort_values('policy_priority_index', ascending=False)
    
    priority_output = priority[['location', 'land_use_type', 'plastic_percent', 'pvc_percent_of_plastic', 
                                'treatability_score', 'policy_priority_index']].head(10)
    
    priority_output.to_csv(OUT / '7h_intervention_prioritization.csv', index=False)
    print("\nTop 5 Policy Intervention Targets (High Burden + High Treatability):")
    print(priority_output.head(5).to_string(index=False))

    # -------------------------------------------------------------------------
    # 2. INFRASTRUCTURE ROUTING SCENARIO SIMULATION
    # -------------------------------------------------------------------------
    print("\n2. Simulating Infrastructure Routing Scenarios...")
    
    # Bawana is over-stressed (108%). Ghazipur (58%) and Tehkhand (68%) are under-utilized.
    # Let's find localities currently routed to Bawana (nearest) that could be diverted.
    
    bawana_catchment = df[df['nearest_wte_facility'] == 'Bawana'].copy()
    
    if len(bawana_catchment) > 0:
        # Calculate diversion cost (extra km to travel to Ghazipur or Tehkhand instead of Bawana)
        bawana_catchment['dist_to_alt_ghazipur'] = bawana_catchment['distance_to_ghazipur'] - bawana_catchment['distance_to_bawana']
        bawana_catchment['dist_to_alt_tehkhand'] = bawana_catchment['distance_to_tehkhand'] - bawana_catchment['distance_to_bawana']
        
        # Find best alternative
        def get_best_alt(row):
            if row['dist_to_alt_ghazipur'] < row['dist_to_alt_tehkhand']:
                return pd.Series(['Ghazipur', row['dist_to_alt_ghazipur']])
            else:
                return pd.Series(['Tehkhand', row['dist_to_alt_tehkhand']])
                
        bawana_catchment[['best_alternative', 'extra_km_cost']] = bawana_catchment.apply(get_best_alt, axis=1)
        
        # Sort by lowest extra km cost to divert
        diversion = bawana_catchment.sort_values('extra_km_cost')
        diversion['extra_km_cost'] = diversion['extra_km_cost'].round(2)
        
        div_out = diversion[['location', 'zone', 'plastic_percent', 'distance_to_bawana', 
                             'best_alternative', 'extra_km_cost']]
                             
        div_out.to_csv(OUT / '7h_bawana_diversion_routing.csv', index=False)
        print("\nOptimal Bawana Diversion Scenario (Lowest Extra Distance):")
        print(div_out.head(5).to_string(index=False))
        
        # Aggregate simulation
        top_3_divert = diversion.head(3)
        mean_extra_km = top_3_divert['extra_km_cost'].mean()
        burden_diverted = top_3_divert['plastic_percent'].mean()
        
        print("\nRouting Simulation Summary:")
        print(f"- Diverting the top 3 optimal localities away from Bawana would only add an average of {mean_extra_km:.1f} km per trip.")
        print(f"- This would shift highly burdened waste (mean {burden_diverted:.1f}% plastic) to under-utilized facilities.")
    else:
        print("No localities in Bawana catchment found.")
        
    print("\n✓ Phase 7H Advanced Policy Analysis Complete.")

if __name__ == "__main__":
    execute_policy_analysis()
