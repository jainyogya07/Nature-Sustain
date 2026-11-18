#!/usr/bin/env python3
"""
=============================================================================
PHASE 7E (FULL): ADVANCED SPATIAL ANALYSIS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Calculates:
1. Spatial Autocorrelation (Moran's I) for Burden and PVC.
2. Spatial Association (ANOVA) for Income and Land Use.
3. NCR-wide Gravity / Distance to WTE facilities.
=============================================================================
"""

import pandas as pd
import numpy as np
from scipy import stats
from math import radians, cos, sin, asin, sqrt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
OUT.mkdir(parents=True, exist_ok=True)

# WTE Facilities
FACILITIES = [
    {"name": "Okhla", "lat": 28.528, "lon": 77.283, "type": "WTE"},
    {"name": "Ghazipur", "lat": 28.625, "lon": 77.327, "type": "WTE"},
    {"name": "Bawana", "lat": 28.799, "lon": 77.050, "type": "Integrated"},
    {"name": "Tehkhand", "lat": 28.513, "lon": 77.279, "type": "WTE"}
]

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance in kilometers between two points."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    return c * r

def calculate_morans_i(y, coords, k=5):
    """
    Calculate Global Moran's I for a variable y given coordinates.
    Uses inverse distance weighting (IDW) for the k nearest neighbors.
    """
    n = len(y)
    y_mean = np.mean(y)
    
    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                d = haversine(coords[i][1], coords[i][0], coords[j][1], coords[j][0])
                dist_matrix[i,j] = d if d > 0 else 0.0001
            else:
                dist_matrix[i,j] = np.inf
                
    # Weight matrix (inverse distance, 1/d)
    w = np.zeros((n, n))
    for i in range(n):
        # Find k nearest neighbors
        nearest = np.argsort(dist_matrix[i])[:k]
        for j in nearest:
            w[i, j] = 1.0 / dist_matrix[i, j]
            
    # Row-standardize weights
    row_sums = w.sum(axis=1)
    for i in range(n):
        if row_sums[i] > 0:
            w[i, :] = w[i, :] / row_sums[i]
            
    W = np.sum(w)
    
    num = 0
    den = np.sum((y - y_mean)**2)
    
    for i in range(n):
        for j in range(n):
            num += w[i,j] * (y[i] - y_mean) * (y[j] - y_mean)
            
    I = (n / W) * (num / den)
    
    # Expected I
    E_I = -1.0 / (n - 1)
    
    return I, E_I

def execute_advanced_spatial():
    print("=" * 70)
    print("PHASE 7E: ADVANCED SPATIAL ANALYSIS")
    print("=" * 70)
    
    # Load data
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df['pvc_percent_of_plastic'] = df['pvc_percent_of_plastic'].fillna(0)
    
    # Filter to localities with valid coordinates
    df_geo = df.dropna(subset=['latitude_decimal', 'longitude_decimal']).copy()
    n = len(df_geo)
    print(f"Loaded {n} localities with valid coordinates.")
    
    # -------------------------------------------------------------------------
    # 1. SPATIAL CLUSTERING (Moran's I)
    # -------------------------------------------------------------------------
    print("\n1. Calculating Spatial Autocorrelation...")
    coords = list(zip(df_geo['latitude_decimal'], df_geo['longitude_decimal']))
    
    # Plastic Burden (plastic_percent)
    y_burden = df_geo['plastic_percent'].values
    I_burden, EI_burden = calculate_morans_i(y_burden, coords, k=5)
    
    # PVC Problematic (pvc_percent_of_plastic)
    y_pvc = df_geo['pvc_percent_of_plastic'].values
    I_pvc, EI_pvc = calculate_morans_i(y_pvc, coords, k=5)
    
    clustering_results = pd.DataFrame([
        {'Variable': 'Plastic Burden %', 'Morans_I': I_burden, 'Expected_I': EI_burden, 
         'Interpretation': 'Clustered' if I_burden > EI_burden + 0.1 else ('Dispersed' if I_burden < EI_burden - 0.1 else 'Random')},
        {'Variable': 'PVC % of Plastic', 'Morans_I': I_pvc, 'Expected_I': EI_pvc,
         'Interpretation': 'Clustered' if I_pvc > EI_pvc + 0.1 else ('Dispersed' if I_pvc < EI_pvc - 0.1 else 'Random')}
    ])
    clustering_results.to_csv(OUT / '7e_spatial_clustering_morans_i.csv', index=False)
    print(clustering_results.to_string(index=False))
    
    # -------------------------------------------------------------------------
    # 2. SPATIAL ASSOCIATION (ANOVA/Kruskal-Wallis)
    # -------------------------------------------------------------------------
    print("\n2. Analyzing Spatial Context Association (Income & Land Use)...")
    
    associations = []
    
    for var in ['plastic_percent', 'pvc_percent_of_plastic']:
        for context in ['income_level', 'land_use_type']:
            groups = [group[var].values for name, group in df_geo.groupby(context) if len(group) > 2]
            
            if len(groups) > 1:
                # Kruskal-Wallis H-test (non-parametric ANOVA)
                stat, p_val = stats.kruskal(*groups)
                sig = "Significant (p<0.05)" if p_val < 0.05 else "Not Significant"
                associations.append({
                    'Metric': var,
                    'Context_Factor': context,
                    'H_Statistic': round(stat, 3),
                    'p_value': round(p_val, 4),
                    'Significance': sig
                })
                
    assoc_df = pd.DataFrame(associations)
    assoc_df.to_csv(OUT / '7e_spatial_association_context.csv', index=False)
    print(assoc_df.to_string(index=False))
    
    # Group means for reporting
    income_means = df_geo.groupby('income_level')[['plastic_percent', 'pvc_percent_of_plastic']].mean().round(2)
    income_means.to_csv(OUT / '7e_income_group_averages.csv')
    
    lu_means = df_geo.groupby('land_use_type')[['plastic_percent', 'pvc_percent_of_plastic']].mean().round(2)
    lu_means.to_csv(OUT / '7e_land_use_group_averages.csv')
    
    # -------------------------------------------------------------------------
    # 3. NCR-WIDE GRAVITY / INFRASTRUCTURE PROXIMITY
    # -------------------------------------------------------------------------
    print("\n3. Calculating Nearest WTE Infrastructure Proximity...")
    
    dist_records = []
    
    for idx, row in df_geo.iterrows():
        lat = row['latitude_decimal']
        lon = row['longitude_decimal']
        loc = row['location']
        burden = row['plastic_percent']
        
        distances = []
        for fac in FACILITIES:
            d = haversine(lon, lat, fac['lon'], fac['lat'])
            distances.append((fac['name'], d))
            
        # Sort by distance
        distances.sort(key=lambda x: x[1])
        nearest_fac, nearest_dist = distances[0]
        
        dist_records.append({
            'locality': loc,
            'zone': row['zone'],
            'plastic_percent': burden,
            'pvc_percent': row['pvc_percent_of_plastic'],
            'nearest_wte_facility': nearest_fac,
            'distance_to_nearest_wte_km': round(nearest_dist, 2),
            'distance_to_okhla': round(next(d for f, d in distances if f == 'Okhla'), 2),
            'distance_to_ghazipur': round(next(d for f, d in distances if f == 'Ghazipur'), 2),
            'distance_to_bawana': round(next(d for f, d in distances if f == 'Bawana'), 2),
            'distance_to_tehkhand': round(next(d for f, d in distances if f == 'Tehkhand'), 2)
        })
        
    df_dist = pd.DataFrame(dist_records)
    df_dist.to_csv(OUT / '7e_infrastructure_proximity.csv', index=False)
    
    # Calculate average burden assigned to each facility's "catchment area"
    catchment = df_dist.groupby('nearest_wte_facility').agg(
        num_localities=('locality', 'count'),
        mean_burden=('plastic_percent', 'mean'),
        mean_pvc=('pvc_percent', 'mean'),
        mean_distance_km=('distance_to_nearest_wte_km', 'mean')
    ).round(2).reset_index()
    
    catchment.to_csv(OUT / '7e_wte_catchment_profiles.csv', index=False)
    print("\nFacility Catchment Profiles (Nearest Neighbor Allocation):")
    print(catchment.to_string(index=False))

    print("\n✓ Phase 7E Advanced Spatial Analysis Complete.")
    print(f"Outputs written to: {OUT}")

if __name__ == "__main__":
    execute_advanced_spatial()
