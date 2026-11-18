#!/usr/bin/env python3
"""
=============================================================================
PHASE 7J: DIAGNOSTIC AUDIT
Delhi-NCR Circular Plastic Assessment
=============================================================================
Validates group sample sizes for statistical tests (Kruskal-Wallis ANOVA).
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

def run_diagnostics():
    print("=" * 70)
    print("PHASE 7J: PRE-ANOVA DIAGNOSTIC AUDIT")
    print("=" * 70)
    
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    
    print("\n1. Income Level Distribution:")
    income_counts = df['income_level'].value_counts()
    print(income_counts)
    if (income_counts < 3).any():
        print("WARNING: Some Income Level groups have N < 3. Kruskal-Wallis power may be low.")
    else:
        print("✓ Income Level variance is sufficient for ANOVA.")
        
    print("\n2. Land Use Type Distribution:")
    lu_counts = df['land_use_type'].value_counts()
    print(lu_counts)
    if len(lu_counts) < 2:
        print("CRITICAL WARNING: Land Use Type has NO variance (only 1 category). ANOVA is invalid.")
    elif (lu_counts < 3).any():
        print("WARNING: Some Land Use Type groups have N < 3. Kruskal-Wallis power may be extremely low.")
    else:
        print("✓ Land Use Type variance is sufficient for ANOVA.")

if __name__ == "__main__":
    run_diagnostics()
