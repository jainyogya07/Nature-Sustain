#!/usr/bin/env python3
"""
=============================================================================
PHASE 8C: LOCAL SPATIAL HOTSPOT ANALYSIS (LISA)
Delhi-NCR Circular Plastic Assessment
=============================================================================
Computes Local Moran's I to identify mathematically significant spatial 
clusters (High-High, Low-Low) instead of relying on arbitrary thresholding.
=============================================================================
"""

import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 6371

def execute_lisa():
    print("=" * 70)
    print("PHASE 8C: LOCAL SPATIAL HOTSPOT ANALYSIS (LISA)")
    print("=" * 70)
    
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df_geo = df.dropna(subset=['latitude_decimal', 'longitude_decimal']).copy().reset_index(drop=True)
    coords = list(zip(df_geo['latitude_decimal'], df_geo['longitude_decimal']))
    n = len(df_geo)
    
    # Weight Matrix (k=5)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                d = haversine(coords[i][1], coords[i][0], coords[j][1], coords[j][0])
                dist_matrix[i,j] = d if d > 0 else 0.0001
            else:
                dist_matrix[i,j] = np.inf
                
    w = np.zeros((n, n))
    for i in range(n):
        nearest = np.argsort(dist_matrix[i])[:5]
        for j in nearest:
            w[i, j] = 1.0 / dist_matrix[i, j]
            
    row_sums = w.sum(axis=1)
    for i in range(n):
        if row_sums[i] > 0:
            w[i, :] = w[i, :] / row_sums[i]
            
    # Calculate LISA for Plastic Burden
    y = df_geo['plastic_percent'].values
    y_mean = np.mean(y)
    y_var = np.var(y)
    z = y - y_mean
    
    local_I = np.zeros(n)
    p_values = np.zeros(n)
    cluster_type = []
    
    permutations = 999
    
    for i in range(n):
        # Observed Local I
        lag = np.sum(w[i] * z)
        local_I[i] = (z[i] / y_var) * lag
        
        # Quadrant
        if z[i] > 0 and lag > 0: quad = 'High-High (Hotspot)'
        elif z[i] < 0 and lag < 0: quad = 'Low-Low (Coldspot)'
        elif z[i] > 0 and lag < 0: quad = 'High-Low (Spatial Outlier)'
        else: quad = 'Low-High (Spatial Outlier)'
        
        # Permutation testing (conditional on i)
        sim_I = np.zeros(permutations)
        z_others = np.delete(z, i)
        w_i = w[i]
        w_others = np.delete(w_i, i)
        
        for p in range(permutations):
            np.random.shuffle(z_others)
            sim_lag = np.sum(w_others * z_others)
            sim_I[p] = (z[i] / y_var) * sim_lag
            
        larger = np.sum(sim_I >= local_I[i]) if local_I[i] > 0 else np.sum(sim_I <= local_I[i])
        p_val = (larger + 1) / (permutations + 1)
        
        # Two-tailed effect, multiply p-value by 2 for safety, cap at 1.0
        p_val = min(p_val * 2, 1.0)
        p_values[i] = p_val
        
        # Significance Thresholds: <0.05 Strong, 0.05-0.10 Marginal
        if p_val < 0.05:
            cluster_type.append(f"Strong {quad}")
        elif p_val <= 0.10:
            cluster_type.append(f"Marginal {quad}")
        else:
            cluster_type.append('Not Significant')
            
    df_geo['Local_Morans_I'] = np.round(local_I, 3)
    df_geo['LISA_P_Value'] = np.round(p_values, 4)
    df_geo['Cluster_Classification'] = cluster_type
    
    hotspots = df_geo[df_geo['Cluster_Classification'] != 'Not Significant'].copy()
    hotspots = hotspots[['location', 'plastic_percent', 'Local_Morans_I', 'LISA_P_Value', 'Cluster_Classification']]
    hotspots = hotspots.sort_values('LISA_P_Value')
    
    hotspots.to_csv(OUT / '8c_lisa_hotspots_elite.csv', index=False)
    
    print(f"\nIdentified {len(hotspots)} strong/marginal local spatial clusters (p <= 0.10):")
    if len(hotspots) > 0:
        print(hotspots.to_string(index=False))
    else:
        print("No significant local clusters detected. Spatial distribution is entirely chaotic.")
        
if __name__ == "__main__":
    execute_lisa()
