#!/usr/bin/env python3
"""
=============================================================================
PHASE 8: DATA INTEGRITY AUDIT
Delhi-NCR Circular Plastic Assessment
=============================================================================
Recalculates exact compositional means directly from the N=55 subset of 
the final dataset to ensure 100% traceability for Table 1.
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"

def execute_integrity_audit():
    print("=" * 70)
    print("PHASE 8: DATA INTEGRITY AUDIT (N=55 Resin Traceability)")
    print("=" * 70)
    
    # 1. Load the final audited dataset
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    
    # Total plastic burden is across all N=58
    mean_burden = round(df['plastic_percent'].mean(), 2)
    
    # Resin composition is across N=55 complete cases
    df_resin = df.dropna(subset=['pet_percent_of_plastic', 'hdpe_ldpe_percent_of_plastic', 'pvc_percent_of_plastic', 'pp_percent_of_plastic'])
    
    print(f"Total Localities (N): {len(df)}")
    print(f"Complete Resin Cases (N): {len(df_resin)}")
    
    mean_pet = round(df_resin['pet_percent_of_plastic'].mean(), 2)
    mean_hdpe = round(df_resin['hdpe_ldpe_percent_of_plastic'].mean(), 2)
    mean_pvc = round(df_resin['pvc_percent_of_plastic'].mean(), 2)
    mean_pp = round(df_resin['pp_percent_of_plastic'].mean(), 2)
    
    print("\nVerified True Sample Means:")
    print(f"Plastic Burden (N=58): {mean_burden}%")
    print(f"PET (N=55): {mean_pet}%")
    print(f"HDPE/LDPE (N=55): {mean_hdpe}%")
    print(f"PVC (N=55): {mean_pvc}%")
    print(f"PP (N=55): {mean_pp}%")

    # 2. Update the Benchmark Matrix
    BENCHMARKS = [
        {
            'Metric': 'plastic_percent',
            'Our_Mean': mean_burden,
            'Benchmark_Range': '8.0 - 10.0',
            'Year': '2020-21',
            'Geography': 'National Metro Average',
            'Methodological_Comparability': 'Manual Physical Characterization',
            'Source': 'CPCB Annual Report on PWM'
        },
        {
            'Metric': 'pet_percent',
            'Our_Mean': mean_pet,
            'Benchmark_Range': '8.0 - 12.0',
            'Year': '2019',
            'Geography': 'Delhi NCT Baseline',
            'Methodological_Comparability': 'Standard Municipal Sampling',
            'Source': 'NEERI Delhi MSW Characterization'
        },
        {
            'Metric': 'hdpe_ldpe_percent',
            'Our_Mean': mean_hdpe,
            'Benchmark_Range': '45.0 - 55.0',
            'Year': '2019',
            'Geography': 'Delhi NCT Baseline',
            'Methodological_Comparability': 'Standard Municipal Sampling',
            'Source': 'NEERI Delhi MSW Characterization'
        },
        {
            'Metric': 'pvc_percent',
            'Our_Mean': mean_pvc,
            'Benchmark_Range': '0.0 - 1.0',
            'Year': '2019',
            'Geography': 'Delhi NCT Baseline',
            'Methodological_Comparability': 'Standard Municipal Sampling',
            'Source': 'NEERI Delhi MSW Characterization'
        },
        {
            'Metric': 'pp_percent',
            'Our_Mean': mean_pp,
            'Benchmark_Range': '10.0 - 15.0',
            'Year': '2019',
            'Geography': 'Delhi NCT Baseline',
            'Methodological_Comparability': 'Standard Municipal Sampling',
            'Source': 'NEERI Delhi MSW Characterization'
        }
    ]
    
    df_bench = pd.DataFrame(BENCHMARKS)
    
    status = []
    
    for _, row in df_bench.iterrows():
        low = float(row['Benchmark_Range'].split(' - ')[0])
        high = float(row['Benchmark_Range'].split(' - ')[1])
        val = row['Our_Mean']
        
        if val < low:
            status.append("Below Baseline")
        elif val > high:
            status.append("Above Baseline")
        else:
            status.append("Concordant")
            
    df_bench['Baseline_Concordance'] = status
    df_bench.to_csv(OUT / '8a_benchmark_provenance_elite.csv', index=False)
    
    print("\n✓ Dynamically recalculated and updated Benchmark Provenance table.")

if __name__ == "__main__":
    execute_integrity_audit()
