#!/usr/bin/env python3
"""
=============================================================================
PHASE 8: FINAL SCIENTIFIC AUDIT
Delhi-NCR Circular Plastic Assessment
=============================================================================
Regenerates the manuscript prose enforcing the 9-step scientific audit.
Replaces definitive causal claims with strict observational framing.
=============================================================================
"""

from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PROSE_FILE = BASE / "FINAL_MANUSCRIPT_PROSE.md"

def generate_audited_prose():
    print("=" * 70)
    print("PHASE 8: REGENERATING AUDITED SCIENTIFIC PROSE")
    print("=" * 70)

    content = r"""# Observational Heterogeneity in Urban Plastic Waste: Micro-Spatial Associations and Infrastructure Logistics Scenarios in Delhi NCT

**Note on Methodological Scope:** N=58 represents the full locality-level observational dataset. N=55 represents the subset of complete cases for detailed resin-level compositional analyses. The three localities excluded from resin-level analyses were excluded because of incomplete compositional observations; consequently, resin-specific estimates should be interpreted as complete-case summaries rather than unbiased estimates for all 58 localities. The spatial and infrastructure footprint is strictly defined as Delhi NCT.

---

## Abstract
Urban solid waste management traditionally relies on macro-level averages, which may obscure critical micro-spatial heterogeneity. This observational study of Delhi NCT (N=58 localities) investigates the spatial, socioeconomic, and infrastructural dimensions of plastic waste generation. While the city-wide average plastic burden (10.82%) exhibits concordance with standard national baselines, this aggregate metric masks statistically significant associations between plastic fraction and local socioeconomic status (Kruskal-Wallis FDR p=0.0116) as well as land-use classification (FDR p=0.0223). Global spatial autocorrelation was non-significant (p=0.247), indicating that pollution does not follow smooth geographical gradients. However, Local Moran's I analysis (LISA) identified isolated, statistically significant micro-spatial hotspots. Under an explicit representativeness assumption, the observed composition translates to a scenario-based physical burden of approximately 1,226 TPD. This study then assesses intervention-priority stability under alternative weighting paradigms. Finally, we translate theoretical distance into a hypothetical operational scenario, demonstrating that shifting high-burden waste from over-stressed to under-utilized infrastructure yields theoretical diversion costs as low as ₹13.33/tonne.

---

## 1. Introduction
The transition to a circular plastic economy is structurally constrained by the granularity of available municipal data. While megacities like Delhi NCT produce approximately 11,328 TPD of municipal solid waste, policy interventions and Extended Producer Responsibility (EPR) targets are frequently modeled against a single homogenized baseline. This paper systematically deconstructs that baseline, mapping the empirical chain from observed compositional heterogeneity to statistical association, priority stability, and operational infrastructure scenarios, explicitly recognizing the methodological limitations inherent in observational data.

## 2. Observed Empirical Findings

### 2.1 Micro-Spatial Socioeconomic Association
Plastic burden exhibits statistically significant micro-spatial associations with demographic zones. Non-parametric Kruskal-Wallis testing, corrected via Benjamini-Hochberg False Discovery Rate (FDR), reveals strong associations with both Income Level ($\epsilon^2$ = 0.208, FDR p=0.0116) and Land-Use Type ($\epsilon^2$ = 0.193, FDR p=0.0223). 

### 2.2 Global Randomness vs. Localized Hotspots
These high-burden areas do not coalesce into a predictable city-wide gradient. Monte Carlo permutation testing (n=999) applied to spatial autocorrelation yielded a non-significant Global Moran's I (I=0.0529, p=0.247). However, Local Moran's I (LISA) analysis—utilizing a k=5 nearest neighbor spatial weight matrix via Haversine distance—successfully extracted localized structures from this global randomness. LISA p-values represent permutation-based local exploratory statistics. Using p < 0.05 for individual local inference and 0.05 ≤ p < 0.10 for marginal/exploratory patterns, we identified strong high-high hotspots such as Kamla Nagar Market (p=0.002) and Tis Hazari Court (p=0.028), alongside exploratory patterns at Ajmal Khan Road (p=0.066).

### 2.3 Scenario-Based Tonnage Extrapolation
Under an explicit representativeness assumption—where the N=58 observational mean corresponds to the 11,328 TPD municipal baseline—the observed composition translates to a scenario-based physical burden of approximately 1,226.1 TPD of total plastic, comprising 652.8 TPD of recyclable HDPE/LDPE and a highly localized 20.2 TPD PVC-bearing fraction. 

### 2.4 Differential Stability of Intervention Priorities
When modeling EPR interventions, policy targets demonstrated massive disparities in algorithmic stability. Sensitivity testing across four alternative weighting paradigms (Baseline Equal Weights, High Vulnerability Focus, High Treatability Focus, and Logistics-Optimized Focus) revealed that top targets like DAV School are structurally stable (Mean Rank = 1.0, SD = 0.0). Conversely, targets like Ryan International School proved highly method-sensitive (SD = 6.90). 

## 3. Inferred Mechanisms & Competing Explanations
The observed socioeconomic associations highlight a critical urban mechanism: plastic generation is deeply entangled with local economic activity. The higher plastic fractions observed in affluent and commercial land-use zones are likely driven by heightened consumption patterns and institutional procurement behaviors. 

However, because this is a cross-sectional observational study, the data cannot strictly isolate causation. An alternative mechanism for the higher observed plastic percentage in affluent localities is differential municipal collection efficiency. If organic and heavy inert waste is cleared more aggressively in high-income neighborhoods (leaving lighter, bulky plastics behind in secondary collection points), the *relative* percentage of plastic will artificially inflate, even if absolute per-capita generation remains constant. External benchmark concordance supports the plausibility of our observed composition, though it does not eliminate localized sampling variance.

Furthermore, the emergence of isolated LISA hotspots confirms that commercially classified locations coincide with localized concentrations of observed plastic burden, challenging the assumption of uniform spatial diffusion.

## 4. Policy Scenarios and Translation
Unlike traditional macro-level solid waste assessments, this study demonstrates that plastic burden exhibits statistically significant micro-spatial associations with socioeconomic and land-use contexts. 

By mapping this heterogeneity onto the existing Waste-to-Energy infrastructure network, we identified specific, actionable intervention opportunities. Under a hypothetical operational scenario assuming optimal 9-tonne payloads and flat ₹50/km round-trip transport costs, diverting specific high-burden localities away from the over-stressed Bawana facility toward under-utilized alternatives (e.g., Tehkhand) yields theoretical diversion costs ranging from ₹13 to ₹40/tonne. These values represent transport-cost scenarios under fixed routing and payload assumptions and should not be interpreted as realized municipal operating costs or profitability estimates. However, the policy implication indicates that municipalities could evaluate a shift from uniform city-wide EPR quotas toward localized, precision-targeted logistics interventions.
"""

    with open(PROSE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Audited Final Manuscript Prose successfully generated and saved to: {PROSE_FILE}")

if __name__ == "__main__":
    generate_audited_prose()
