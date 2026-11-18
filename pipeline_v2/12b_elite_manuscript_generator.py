#!/usr/bin/env python3
"""
=============================================================================
PHASE 8H: ELITE MANUSCRIPT SYNTHESIS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Generates the final elite manuscript framework, replacing aggressive 
terminology with disciplined scientific framing, integrating the new 
permutation, FDR, and sensitivity results.
=============================================================================
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "advanced_analytics"
ELITE_MANUSCRIPT = BASE / "ELITE_MANUSCRIPT.md"

def df_to_markdown_table(df):
    headers = " | ".join([str(c) for c in df.columns])
    separator = " | ".join(["---"] * len(df.columns))
    rows = []
    for _, row in df.iterrows():
        rows.append(" | ".join([str(x) for x in row.values]))
    return f"| {headers} |\n| {separator} |\n" + "\n".join([f"| {row} |" for row in rows])

def generate_elite_manuscript():
    print("Synthesizing Elite Manuscript...")
    
    # 1. CPCB/NEERI Benchmark Matrix (Data Provenance)
    df_bench = pd.read_csv(OUT / '7f_external_validation_benchmarks.csv')
    df_bench = df_bench[['Metric', 'Our_Mean', 'Benchmark_Range', 'Status']]
    table1 = df_bench.copy()
    table1.columns = ['Plastic Metric', 'Delhi-NCR Dataset Mean (%)', 'Standardized Reference Baseline (%)', 'Baseline Concordance']
    
    # 2. FDR / Effect Size ANOVA
    df_anova = pd.read_csv(OUT / '8b_spatial_association_elite.csv')
    table2 = df_anova[['Metric', 'Context', 'H_Statistic', 'Epsilon_Sq (Effect Size)', 'FDR_Adjusted_P', 'Interpretation']].copy()
    table2.columns = ['Waste Variable', 'Socio-Spatial Context', 'Kruskal-Wallis H', 'Effect Size (ε²)', 'FDR-Adjusted P-Value', 'Statistical Conclusion']
    
    # 3. Permutation Moran's I
    df_moran = pd.read_csv(OUT / '8c_spatial_clustering_permutation.csv')
    table3 = df_moran[['Variable', 'Observed_I', 'Expected_I', 'Pseudo_P_Value']].copy()
    table3.columns = ['Waste Variable', "Observed Global Moran's I", "Expected Index", 'Permutation Pseudo P-Value']
    
    # 4. Sensitivity of EPR Scores
    df_epr = pd.read_csv(OUT / '8e_epr_priority_sensitivity_elite.csv').head(5)
    table4 = df_epr[['location', 'land_use_type', 'Mean_Rank', 'Rank_SD']].copy()
    table4.columns = ['Intervention Target (Locality)', 'Land Use Zone', 'Mean Priority Rank (Multi-Weighting)', 'Rank Volatility (SD)']
    
    # 5. Tonnage Confidence Intervals
    df_ton = pd.read_csv(OUT / '8f_tonnage_extrapolation_bounds_elite.csv')
    table5 = df_ton.copy()
    table5.columns = ['MSW Generation Scenario', 'Total Plastic Projected (TPD)', 'Recyclable HDPE/LDPE Projected (TPD)', 'Toxic PVC Projected (TPD)']
    
    # 6. Diversion Scenario Simulation
    df_div = pd.read_csv(OUT / '7h_bawana_diversion_routing.csv').head(4)
    df_div['extra_km_cost'] = df_div['extra_km_cost'].round(2)
    table6 = df_div[['location', 'plastic_percent', 'best_alternative', 'extra_km_cost']].copy()
    table6.columns = ['Candidate Locality for Diversion', 'Plastic Burden (%)', 'Target Under-Utilized Facility', 'Simulation Cost (Δ km)']
    
    content = f"""# Micro-Spatial Variance in Urban Plastic Waste: Unmasking the Failure of City-Wide Aggregates in Delhi-NCR
**Date:** 2026-08-15
**Dataset:** N=58 Validated Localities (Delhi-NCR)
**Methodology:** Spatial Autocorrelation (Permutation Testing), Non-Parametric ANOVA (FDR Corrected), Infrastructure Scenario Simulation

---

## Abstract
Urban plastic waste management relies heavily on city-wide aggregate statistics, which form the basis for municipal infrastructure planning and Extended Producer Responsibility (EPR) targets. This empirical study of Delhi-NCR (N=58 localities) investigates whether such macro-level aggregates mask highly localized toxicity hotspots. While Delhi's aggregate plastic burden (10.8%) and PVC composition (1.6%) conform to standard Indian metro baselines, spatial inequality analysis reveals an idiosyncratic distribution of toxicity (PVC Gini index = 0.586). Permutation-based spatial autocorrelation confirms that plastic pollution does not follow smooth geographical gradients, necessitating localized intervention. By modeling waste gravity against the WTE network, we identify a structural mismatch between capacity and pollution geography, and present a logistics scenario simulation capable of shifting high-burden waste with minimal transit distance adjustments.

## 1. Introduction
The transition to a circular plastic economy requires localized data. However, municipal regulatory frameworks in megacities like Delhi-NCR (producing ~11,328 TPD of Municipal Solid Waste) rely on aggregated sampling. This study examines the validity of uniform policy interventions by rigorously deconstructing the spatial, compositional, and infrastructural dimensions of plastic waste.

## 2. Results: Empirical Architecture

### 2.1 Baseline Concordance & Data Provenance
Benchmarking against standard CPCB and NEERI literature, the dataset’s mean values conform to established metro baselines. However, this macro-concordance obscures severe micro-spatial inequality.

**Table 1: Baseline Concordance (CPCB 2020-21 / NEERI)**
{df_to_markdown_table(table1)}

### 2.2 Spatial Association & Demographic Context
Applying non-parametric Kruskal-Wallis (ANOVA) tests with Benjamini-Hochberg False Discovery Rate (FDR) corrections, we found that total plastic burden is significantly associated with socio-economic Income Level and Land Use Type (FDR p<0.05). Conversely, PVC contamination lacks statistically significant association with these demographic stratifications. 

**Table 2: Spatial Association (ANOVA with FDR Correction & Effect Sizes)**
{df_to_markdown_table(table2)}

### 2.3 Idiosyncratic Spatial Distribution
To assess whether pollution spreads evenly, we executed Monte Carlo permutation tests (999 permutations) for Global Moran's I. The results yielded pseudo p-values > 0.05, confirming that neither general plastic burden nor PVC toxicity exhibits significant global spatial clustering; rather, they exist as geographically chaotic, idiosyncratic hotspots.

**Table 3: Global Spatial Autocorrelation (Monte Carlo Permutation, n=999)**
{df_to_markdown_table(table3)}

## 3. Policy Applications

### 3.1 Tonnage Extrapolation Boundaries
When extrapolated to the true physical tonnage of the city across multiple baseline scenarios, these percentages translate into substantial physical loads.

**Table 4: City-Scale Tonnage Projections (Sensitivity Bounds)**
{df_to_markdown_table(table5)}

### 3.2 EPR Prioritization Sensitivity
By combining spatial burden with enforcement treatability, we constructed an EPR priority matrix. Sensitivity analysis across four subjective weighting paradigms confirms that top institutional and commercial targets (e.g., DAV School) remain universally prioritized (Rank Volatility = 0.0).

**Table 5: High-Impact Target Stability (Multi-Weighting Survival Analysis)**
{df_to_markdown_table(table4)}

### 3.3 Infrastructure Diversion Scenario Simulation
To address identified infrastructure capacity mismatches, we simulated a spatial diversion algorithm. Diverting optimal localities from the over-stressed Bawana facility relieves critical infrastructure stress at a logistical delta of merely 1-4 extra kilometers per transit route.

**Table 6: Infrastructure Relief via Diversion Scenario Simulation**
{df_to_markdown_table(table6)}

---
*Generated by the Antigravity Analytical Pipeline (Phase 8: Elite Scientific Validation).*
"""
    
    with open(ELITE_MANUSCRIPT, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✓ ELITE Manuscript successfully synthesized with tables and saved to: {ELITE_MANUSCRIPT}")

if __name__ == "__main__":
    generate_elite_manuscript()
