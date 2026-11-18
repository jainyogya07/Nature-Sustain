#!/usr/bin/env python3
"""
=============================================================================
PHASE 8B & 8C: ELITE SPATIAL & STATISTICAL VALIDATION
Delhi-NCR Circular Plastic Assessment
=============================================================================
1. Moran's I with Monte Carlo Permutation Testing
2. Kruskal-Wallis with Epsilon-Squared Effect Sizes
3. Benjamini-Hochberg FDR Multiple-Testing Correction
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

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r

def calculate_morans_i_manual(y, dist_matrix, w_matrix, n, W):
    y_mean = np.mean(y)
    num = 0
    den = np.sum((y - y_mean)**2)
    
    if den == 0: return 0.0
    
    for i in range(n):
        for j in range(n):
            if w_matrix[i,j] > 0:
                num += w_matrix[i,j] * (y[i] - y_mean) * (y[j] - y_mean)
                
    I = (n / W) * (num / den)
    return I

def morans_i_permutation(y, coords, k=5, permutations=999):
    n = len(y)
    
    # Distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                d = haversine(coords[i][1], coords[i][0], coords[j][1], coords[j][0])
                dist_matrix[i,j] = d if d > 0 else 0.0001
            else:
                dist_matrix[i,j] = np.inf
                
    # Weight matrix
    w = np.zeros((n, n))
    for i in range(n):
        nearest = np.argsort(dist_matrix[i])[:k]
        for j in nearest:
            w[i, j] = 1.0 / dist_matrix[i, j]
            
    # Row-standardize weights
    row_sums = w.sum(axis=1)
    for i in range(n):
        if row_sums[i] > 0:
            w[i, :] = w[i, :] / row_sums[i]
            
    W = np.sum(w)
    
    # Observed I
    obs_I = calculate_morans_i_manual(y, dist_matrix, w, n, W)
    E_I = -1.0 / (n - 1)
    
    # Permutations
    sim_I = np.zeros(permutations)
    y_perm = np.copy(y)
    for p in range(permutations):
        np.random.shuffle(y_perm)
        sim_I[p] = calculate_morans_i_manual(y_perm, dist_matrix, w, n, W)
        
    # Pseudo p-value
    larger = np.sum(sim_I >= obs_I)
    p_value = (larger + 1) / (permutations + 1)
    
    return obs_I, E_I, p_value

def fdr_correction(p_values):
    """Benjamini-Hochberg FDR correction."""
    n = len(p_values)
    ranked_indices = np.argsort(p_values)
    ranked_p = np.array(p_values)[ranked_indices]
    
    fdr_p = np.zeros(n)
    for k, p in enumerate(ranked_p):
        q = (p * n) / (k + 1)
        fdr_p[ranked_indices[k]] = q
        
    # Enforce monotonicity
    for k in range(n-2, -1, -1):
        idx = ranked_indices[k]
        next_idx = ranked_indices[k+1]
        fdr_p[idx] = min(fdr_p[idx], fdr_p[next_idx])
        
    return np.minimum(fdr_p, 1.0)

def execute_elite_spatial_stats():
    print("=" * 70)
    print("PHASE 8B/8C: ELITE SPATIAL STATS")
    print("=" * 70)
    
    df = pd.read_csv(BASE / 'pipeline_v2/locality_plastic_analysis_v2.csv')
    df_geo = df.dropna(subset=['latitude_decimal', 'longitude_decimal']).copy()
    coords = list(zip(df_geo['latitude_decimal'], df_geo['longitude_decimal']))
    
    # 1. Permutation Moran's I
    print("\n1. Running Monte Carlo Permutation Spatial Autocorrelation...")
    y_burden = df_geo['plastic_percent'].values
    y_pvc = df_geo['pvc_percent_of_plastic'].fillna(0).values
    
    I_b, E_b, p_b = morans_i_permutation(y_burden, coords)
    I_p, E_p, p_p = morans_i_permutation(y_pvc, coords)
    
    moran_res = pd.DataFrame([
        {'Variable': 'Plastic Burden %', 'Observed_I': round(I_b, 4), 'Expected_I': round(E_b, 4), 'Pseudo_P_Value': round(p_b, 4)},
        {'Variable': 'PVC % of Plastic', 'Observed_I': round(I_p, 4), 'Expected_I': round(E_p, 4), 'Pseudo_P_Value': round(p_p, 4)}
    ])
    moran_res.to_csv(OUT / '8c_spatial_clustering_permutation.csv', index=False)
    print(moran_res.to_string(index=False))
    
    # 2. ANOVA with Effect Sizes & FDR
    print("\n2. Running ANOVA with Effect Sizes and FDR Correction...")
    associations = []
    p_vals_raw = []
    
    for var in ['plastic_percent', 'pvc_percent_of_plastic']:
        for context in ['income_level', 'land_use_type']:
            valid_df = df_geo.dropna(subset=[context, var])
            groups = [group[var].values for name, group in valid_df.groupby(context) if len(group) >= 3]
            
            if len(groups) > 1:
                stat, p_val = stats.kruskal(*groups)
                # Effect size epsilon squared = (H - k + 1) / (n - k)
                n_total = sum(len(g) for g in groups)
                k_groups = len(groups)
                eps_sq = (stat - k_groups + 1) / (n_total - k_groups)
                
                associations.append({
                    'Metric': var,
                    'Context': context,
                    'H_Statistic': round(stat, 3),
                    'Epsilon_Sq (Effect Size)': max(round(eps_sq, 3), 0.0),
                    'Raw_P': p_val
                })
                p_vals_raw.append(p_val)
                
    # Apply FDR
    fdr_p = fdr_correction(p_vals_raw)
    
    for i, assoc in enumerate(associations):
        assoc['FDR_Adjusted_P'] = round(fdr_p[i], 4)
        assoc['Raw_P'] = round(assoc['Raw_P'], 4)
        assoc['Interpretation'] = 'Significant Association' if fdr_p[i] < 0.05 else 'No Significant Association'
        
    assoc_df = pd.DataFrame(associations)
    assoc_df.to_csv(OUT / '8b_spatial_association_elite.csv', index=False)
    print(assoc_df.to_string(index=False))
    
    # 3. Correlations with FDR
    print("\n3. Running Polymer Correlations with FDR Correction...")
    corr_results = []
    corr_p_raw = []
    
    polymers = ['pet_percent_of_plastic', 'hdpe_ldpe_percent_of_plastic', 'pvc_percent_of_plastic', 'pp_percent_of_plastic', 'ps_percent_of_plastic']
    for poly in polymers:
        valid_df = df_geo.dropna(subset=['plastic_percent', poly])
        if len(valid_df) > 5:
            rho, p_val = stats.spearmanr(valid_df['plastic_percent'], valid_df[poly])
            corr_results.append({
                'Polymer': poly.replace('_percent_of_plastic', ''),
                'Spearman_Rho': round(rho, 3),
                'Raw_P': p_val
            })
            corr_p_raw.append(p_val)
            
    fdr_corr_p = fdr_correction(corr_p_raw)
    
    for i, res in enumerate(corr_results):
        res['FDR_Adjusted_P'] = round(fdr_corr_p[i], 4)
        res['Raw_P'] = round(res['Raw_P'], 4)
        res['Interpretation'] = 'Significant Correlation' if fdr_corr_p[i] < 0.05 else 'Insignificant Correlation'
        
    corr_df = pd.DataFrame(corr_results)
    corr_df.to_csv(OUT / '8b_burden_composition_correlation_elite.csv', index=False)
    print(corr_df.to_string(index=False))
    
    print("\n✓ Phase 8B/8C Complete.")

if __name__ == "__main__":
    execute_elite_spatial_stats()
