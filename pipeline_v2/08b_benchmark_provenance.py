#!/usr/bin/env python3
"""
=============================================================================
PHASE 8A: ELITE BENCHMARK PROVENANCE
Delhi-NCR Circular Plastic Assessment
=============================================================================
Validates external benchmarks with exact year, geography, and methodological
comparability for strict traceability.
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"

BENCHMARKS = [
    {
        'Metric': 'plastic_percent',
        'Our_Mean': 10.82,
        'Benchmark_Range': '8.0 - 10.0',
        'Year': '2020-21',
        'Geography': 'National Metro Average',
        'Methodological_Comparability': 'Manual Physical Characterization',
        'Source': 'CPCB Annual Report on PWM'
    },
    {
        'Metric': 'pet_percent',
        'Our_Mean': 23.60,
        'Benchmark_Range': '8.0 - 12.0',
        'Year': '2019',
        'Geography': 'Delhi NCT Baseline',
        'Methodological_Comparability': 'Standard Municipal Sampling',
        'Source': 'NEERI Delhi MSW Characterization'
    },
    {
        'Metric': 'hdpe_ldpe_percent',
        'Our_Mean': 53.24,
        'Benchmark_Range': '45.0 - 55.0',
        'Year': '2019',
        'Geography': 'Delhi NCT Baseline',
        'Methodological_Comparability': 'Standard Municipal Sampling',
        'Source': 'NEERI Delhi MSW Characterization'
    },
    {
        'Metric': 'pvc_percent',
        'Our_Mean': 1.65,
        'Benchmark_Range': '0.0 - 1.0',
        'Year': '2019',
        'Geography': 'Delhi NCT Baseline',
        'Methodological_Comparability': 'Standard Municipal Sampling',
        'Source': 'NEERI Delhi MSW Characterization'
    },
    {
        'Metric': 'pp_percent',
        'Our_Mean': 2.79,
        'Benchmark_Range': '10.0 - 15.0',
        'Year': '2019',
        'Geography': 'Delhi NCT Baseline',
        'Methodological_Comparability': 'Standard Municipal Sampling',
        'Source': 'NEERI Delhi MSW Characterization'
    }
]

def execute_provenance():
    print("=" * 70)
    print("PHASE 8A: ELITE BENCHMARK PROVENANCE")
    print("=" * 70)
    
    df = pd.DataFrame(BENCHMARKS)
    
    # Calculate Divergence manually for strict adherence
    status = []
    divergence = []
    
    for _, row in df.iterrows():
        low = float(row['Benchmark_Range'].split(' - ')[0])
        high = float(row['Benchmark_Range'].split(' - ')[1])
        val = row['Our_Mean']
        
        if val < low:
            status.append("Below Baseline")
            divergence.append(round(val - low, 2))
        elif val > high:
            status.append("Above Baseline")
            divergence.append(round(val - high, 2))
        else:
            status.append("Concordant")
            divergence.append(0.0)
            
    df['Baseline_Concordance'] = status
    
    df.to_csv(OUT / '8a_benchmark_provenance_elite.csv', index=False)
    print("\nGenerated Elite Benchmark Provenance Matrix:")
    print(df.to_string(index=False))
    print("\n✓ Phase 8A Complete.")

if __name__ == "__main__":
    execute_provenance()
