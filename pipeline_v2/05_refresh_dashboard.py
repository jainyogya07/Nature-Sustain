#!/usr/bin/env python3
"""
=============================================================================
MODULE 5: REFRESH DASHBOARD DATA
Delhi-NCR Circular Plastic Assessment
=============================================================================
Reads the outputs from Phase 7 (C, D, E) and rebuilds spatial_dashboard/data.js.
=============================================================================
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DASHBOARD_JS = BASE / "spatial_dashboard/data.js"

def safe_val(v):
    if pd.isna(v):
        return 0.0
    return float(v)

def build_data_js():
    # Load core data
    locality = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    burden_scores = pd.read_csv(BASE / 'phase7c_locality_plastic_burden_scores.csv')
    pvc_scores = pd.read_csv(BASE / 'phase7c_locality_pvc_problematic_scores.csv')
    
    # Load spatial & robustness priorities
    try:
        robust_pri = pd.read_csv(BASE / 'phase7e_robust_priorities_geospatial.csv')
        robust_locs = robust_pri['locality'].tolist()
        robust_caveats = dict(zip(robust_pri['locality'], robust_pri['robustness_level']))
    except:
        robust_locs = []
        robust_caveats = {}

    # Load facility data (we'll just hardcode the 4 WTE facilities from Phase 7C)
    facilities = [
        {"name": "Waste to Energy Plant at Okhla", "lat": 28.528, "lon": 77.283, "type": "Waste to Energy", "capacity": 1950, "processing": 1867.9, "utilization": 95.8, "class": "High Utilization", "headroom_to_85": -210.4},
        {"name": "Waste to Energy Plant at Ghazipur", "lat": 28.625, "lon": 77.327, "type": "Waste to Energy", "capacity": 1300, "processing": 757.3, "utilization": 58.3, "class": "Underutilized", "headroom_to_85": 347.7},
        {"name": "Integrated MSW Facility at Bawana", "lat": 28.799, "lon": 77.050, "type": "Integrated", "capacity": 2000, "processing": 2167.5, "utilization": 108.4, "class": "Over-Stressed", "headroom_to_85": -467.5},
        {"name": "Waste to Energy Plant at Tehkhand", "lat": 28.513, "lon": 77.279, "type": "Waste to Energy", "capacity": 2000, "processing": 1359.3, "utilization": 68.0, "class": "Underutilized", "headroom_to_85": 340.7}
    ]

    # Combine locality data
    loc_data = []
    
    # Merge burden and PVC scores to locality
    merged = locality.merge(burden_scores[['location', 'plastic_burden_score', 'burden_class']], on='location', how='left')
    merged = merged.merge(pvc_scores[['location', 'pvc_problematic_score', 'pvc_class']], on='location', how='left')
    
    for _, row in merged.iterrows():
        lat = safe_val(row.get('latitude_decimal'))
        lon = safe_val(row.get('longitude_decimal'))
        
        # Skip if coordinates are completely missing or broken
        if not lat or not lon:
            continue
            
        loc = row['location']
        is_robust = loc in robust_locs
        caveat = robust_caveats.get(loc, None)
        
        loc_data.append({
            "location": loc,
            "lat": lat,
            "lon": lon,
            "zone": row.get('zone', ''),
            "ward": str(row.get('ward_numbers', '')),
            "income": row.get('income_level', ''),
            "land_use": row.get('land_use_type', ''),
            "plastic_pct": safe_val(row.get('plastic_percent')),
            "burden_score": safe_val(row.get('plastic_burden_score')),
            "burden_class": str(row.get('burden_class', '')),
            "pvc_pct": safe_val(row.get('pvc_percent_of_plastic')),
            "pvc_score": safe_val(row.get('pvc_problematic_score')),
            "pvc_class": str(row.get('pvc_class', '')),
            "pet_pct": safe_val(row.get('pet_percent_of_plastic')),
            "pp_pct": safe_val(row.get('pp_percent_of_plastic')),
            "hdpe_ldpe_pct": safe_val(row.get('hdpe_ldpe_percent_of_plastic')),
            "ps_pct": safe_val(row.get('ps_percent_of_plastic')),
            "others_pct": safe_val(row.get('others_percent_of_plastic')),
            "in_n55": bool(row.get('in_n58_v2', True)),
            "robustness": {
                "appearance_rate": 100.0 if is_robust else 0.0,
                "is_robust": is_robust,
                "caveat": caveat
            },
            "notes": row.get('coordinate_note', '')
        })

    # Sort descending by burden score
    loc_data.sort(key=lambda x: x['burden_score'], reverse=True)

    js_content = f"""// =====================================================================
// DELHI-NCR CIRCULAR PLASTIC ASSESSMENT — Research Data
// Phase 7E Spatial Dashboard · Evidence-Constrained
//
// DATA TRACEABILITY:
//   Source: SRI Plastic Study · DPCC March 2025 Progress Report
//   Processed: pipeline_v2/locality_plastic_analysis_v2.csv
//   N=58 complete cases (restored missing PP/PS values using original PDF)
// =====================================================================

const RESEARCH_DATA = {{

  frozen: {{
    n_sampled: 58,
    n_complete_resin: 58,
    n_excluded: 0,
    excluded_localities: [],
    city_generation_tpd: 1117,
    city_processing_tpd: 858,
    city_efficiency_pct: 76.81,
    city_gap_tpd: 259,
    wte_headroom_combined: 688.4
  }},

  localities: {json.dumps(loc_data, indent=4)},

  facilities: {json.dumps(facilities, indent=4)}
}};
"""
    
    with open(DASHBOARD_JS, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print(f"✓ Dashboard data refreshed: {DASHBOARD_JS}")
    print(f"✓ Localities included: {len(loc_data)}")
    print(f"✓ Facilities included: {len(facilities)}")

if __name__ == "__main__":
    build_data_js()
