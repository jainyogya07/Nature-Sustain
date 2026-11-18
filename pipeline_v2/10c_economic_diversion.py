#!/usr/bin/env python3
"""
=============================================================================
PHASE 8D & 8E: ELITE ECONOMIC MODELING & PRIORITY STABILITY
Delhi-NCR Circular Plastic Assessment
=============================================================================
1. EPR Priority Stability classification.
2. Logistics Financial Cost Calculation (₹/tonne).
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"

def execute_economic_validation():
    print("=" * 70)
    print("PHASE 8D/8E: ECONOMIC & PRIORITY STABILITY VALIDATION")
    print("=" * 70)
    
    # 1. EPR Priority Stability
    df_epr = pd.read_csv(OUT / '8e_epr_priority_sensitivity_elite.csv')
    df_epr['Stability_Status'] = df_epr['Rank_SD'].apply(lambda sd: '🟢 Highly Stable' if sd < 2.0 else ('🟡 Method-Sensitive' if sd < 4.0 else '🔴 Highly Sensitive'))
    df_epr.to_csv(OUT / '8e_epr_priority_stability_elite.csv', index=False)
    print("\n1. EPR Priority Stability:")
    print(df_epr[['location', 'Mean_Rank', 'Rank_SD', 'Stability_Status']].head(6).to_string(index=False))
    
    # 2. Logistics Financial Cost Calculation
    # Assumptions:
    TRUCK_CAPACITY_TONNES = 9.0
    COST_PER_KM_INR = 50.0
    
    df_div = pd.read_csv(OUT / '7h_bawana_diversion_routing.csv')
    
    # Cost = (Delta KM * 2 [round trip] * Cost_per_KM) / Capacity
    df_div['financial_cost_inr_per_tonne'] = (df_div['extra_km_cost'] * 2 * COST_PER_KM_INR) / TRUCK_CAPACITY_TONNES
    df_div['financial_cost_inr_per_tonne'] = df_div['financial_cost_inr_per_tonne'].round(2)
    
    df_div = df_div.sort_values('financial_cost_inr_per_tonne')
    df_div.to_csv(OUT / '8e_economic_diversion_cost_elite.csv', index=False)
    
    print("\n2. Logistics Diversion Scenario (Financial Cost):")
    print(df_div[['location', 'extra_km_cost', 'financial_cost_inr_per_tonne']].head(5).to_string(index=False))
    print(f"\nAssumptions: {TRUCK_CAPACITY_TONNES}t capacity, ₹{COST_PER_KM_INR}/km transport cost.")
    print("\n✓ Phase 8D/8E Complete.")

if __name__ == "__main__":
    execute_economic_validation()
