#!/usr/bin/env python3
"""
=============================================================================
PHASE 8H: SCIENTIFIC NARRATIVE SYNTHESIS
Delhi-NCR Circular Plastic Assessment
=============================================================================
Programmatically generates the final 13+ IF quality manuscript prose, 
weaving the 5 core findings into a cohesive, causally disciplined narrative.
=============================================================================
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROSE_FILE = BASE / "FINAL_MANUSCRIPT_PROSE.md"

def generate_prose():
    print("=" * 70)
    print("PHASE 8H: GENERATING SCIENTIFIC NARRATIVE SYNTHESIS")
    print("=" * 70)

    content = r"""# Micro-Spatial Inequality in Urban Plastic Waste: Linking Observational Heterogeneity to Infrastructure Logistics in Delhi NCT

**Note on Methodological Scope:** N=58 represents the full locality-level observational dataset. N=55 represents the subset of complete cases for detailed resin-level compositional analyses. The spatial and infrastructure footprint is strictly defined as Delhi NCT.

---

## Abstract
Urban solid waste management traditionally relies on macro-level averages, obscuring critical micro-spatial heterogeneity. This observational study of Delhi NCT (N=58 localities) investigates the spatial, socioeconomic, and infrastructural dimensions of plastic waste generation. While city-wide plastic burden (10.82%) conforms to standard national baselines, this aggregate metric masks statistically significant associations between plastic fraction and local socioeconomic status (Kruskal-Wallis FDR p=0.0116) as well as land-use classification (FDR p=0.0223). Notably, global spatial autocorrelation proved non-significant (p=0.247), indicating that pollution does not follow smooth geographical gradients. Instead, Local Moran's I analysis (LISA) successfully identified isolated, statistically significant micro-spatial hotspots. By translating these compositional variances into physical tonnage scenarios (1,226 TPD plastic load), this study assesses intervention-priority stability under alternative weighting paradigms, distinguishing structurally stable policy targets from method-sensitive priorities. Finally, we translate theoretical distance into operational logistics, demonstrating that shifting high-burden waste from over-stressed to under-utilized infrastructure carries a highly viable margin of just ₹13.33/tonne.

---

## 1. Introduction
The transition to a circular plastic economy is structurally constrained by the granularity of available municipal data. While megacities like Delhi NCT produce approximately 11,328 TPD of municipal solid waste, policy interventions and Extended Producer Responsibility (EPR) targets are frequently modeled against a single homogenized baseline. This paper systematically deconstructs that baseline, mapping the empirical chain from observed compositional heterogeneity to statistical association, priority stability, and finally, operational infrastructure economics.

## 2. Headline Findings

### 2.1 Micro-Spatial Socioeconomic Inequality (Finding A)
Plastic burden exhibits statistically significant micro-spatial associations with demographic zones. Non-parametric Kruskal-Wallis testing, corrected via Benjamini-Hochberg False Discovery Rate (FDR), reveals strong associations with both Income Level ($\epsilon^2$ = 0.208, FDR p=0.0116) and Land-Use Type ($\epsilon^2$ = 0.193, FDR p=0.0223). 

### 2.2 Global Randomness vs. Localized Hotspots (Finding B)
Crucially, these high-burden areas do not coalesce into a single, predictable city-wide cluster. Global spatial autocorrelation proved non-significant (Moran's I = 0.0529, permutation p=0.247). However, Local Moran's I (LISA) analysis successfully extracted mathematically significant localized structures from this global randomness, identifying strong high-high hotspots such as Kamla Nagar Market (p=0.002) and Tis Hazari Court (p=0.028).

### 2.3 Composition translates into Physical Burden (Finding C)
These percentages are not merely abstract compositions; they dictate municipal infrastructure stress. Modeled against the Delhi NCT baseline scenario (11,328 TPD), the dataset extrapolates to a physical burden of approximately 1,226.1 TPD of total plastic, comprising 652.8 TPD of recyclable HDPE/LDPE and a highly localized 20.2 TPD PVC-bearing fraction. 

### 2.4 Intervention Priorities exhibit Differential Stability (Finding D)
When modeling EPR interventions, policy targets demonstrated massive disparities in algorithmic stability. Sensitivity testing across four alternative weighting paradigms revealed that top targets like DAV School are structurally stable (Mean Rank = 1.0, SD = 0.0), maintaining absolute priority regardless of subjective scoring. Conversely, targets like Ryan International School proved highly method-sensitive (SD = 6.90). 

### 2.5 Infrastructure Interventions are Economically Viable (Finding E)
Instead of simply calling for broad, multi-million dollar infrastructure expansion, this spatial variance allows for precise logistics rerouting. Diverting specific high-burden localities away from the over-stressed Bawana facility toward under-utilized alternatives (e.g., Tehkhand) can be achieved at minimal operational logistics costs (e.g., ₹13.33/tonne for Dwarka Sector-12, explicitly assuming round-trip transport).

---

## 3. Mechanism Interpretation and Competing Explanations
The observed socioeconomic associations (Finding A) highlight a critical urban mechanism: plastic generation is deeply entangled with local economic activity. The higher plastic fractions observed in affluent and commercial land-use zones are likely driven by heightened consumption patterns, heavily packaged e-commerce penetration, and institutional procurement behaviors. 

However, we must address critical competing explanations. Because this is an observational study, the data cannot strictly isolate causation. An alternative mechanism for the higher observed plastic percentage in affluent localities is differential municipal collection efficiency. If organic and heavy inert waste is cleared more aggressively in high-income neighborhoods (leaving lighter, bulky plastics behind in secondary collection points), the *relative* percentage of plastic will artificially inflate, even if absolute per-capita generation remains constant. While we control for general sample methodology (N=58), this interplay between consumption and municipal clearing rates prevents us from claiming strict causality.

Furthermore, the lack of global spatial autocorrelation (Finding B) challenges the assumption that wealth smoothly diffuses outward in concentric urban rings. Instead, the emergence of isolated LISA hotspots confirms that commercial zoning (e.g., Kamla Nagar) creates highly localized, disjointed gravity wells for packaging waste.

---

## 4. Policy Translation and Novelty Synthesis
The traditional solid waste paradigm asks, "How much plastic does Delhi generate?" This study proves that such a question fundamentally misdiagnoses the problem.

Unlike traditional macro-level solid waste assessments, this study demonstrates that plastic burden exhibits statistically significant micro-spatial associations with socioeconomic and land-use contexts. We show that city-wide averages obscure the true nature of urban pollution, which exists as chaotic, mathematically identifiable local hotspots rather than smooth geographical gradients. 

By mapping this heterogeneity onto the existing Waste-to-Energy infrastructure network, we identify specific, actionable, and financially quantifiable intervention opportunities. The policy implication is clear: municipalities should shift from uniform city-wide EPR quotas to hyper-localized, precision-targeted logistics rerouting, addressing structural inequalities at an operationally viable marginal transport cost.
"""

    with open(PROSE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Final Manuscript Prose successfully generated and saved to: {PROSE_FILE}")

if __name__ == "__main__":
    generate_prose()
