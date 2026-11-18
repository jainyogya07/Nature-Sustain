# DATA_DICTIONARY.md

Every variable used in this manuscript, with type, role, and limitation explicitly stated.

## Layer A: Locality material burden and composition (Phase 7A/7B)

| Variable | Definition | Unit | Obs. level | N | Raw/Derived | Direction | Role | Source | Missing data | Calculation | Interpretation | Limitation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Locality | Sampled site name | categorical | locality | 58 | Raw | n/a | Identifier | Phase 7A | n/a | n/a | Sampling unit | Not a census; 58-site frame |
| Plastic % (raw) | Plastic share, all 58 sites | % | locality | 58 | Raw | Higher=more burden | Context only | Phase 7A | n/a | Direct measurement | Includes Kamla Nehru Ridge (30.49%, excluded from N=55) | Not used for ranking |
| Plastic % (validated) | Plastic share, complete-case sites | % | locality | 55 | Raw | Higher=more burden | Scored (burden) | Phase 7B | 3 excluded | Direct measurement | Basis for burden score | N=55 only |
| Plastic burden score | Normalized plastic % | 0-1 | locality | 55 | Derived | Higher=more burden | Scored (burden) | Phase 7B | n/a | value/max(value) | Relative ranking within N=55 | Not an absolute recyclability measure |
| PET % | Polyethylene terephthalate share | % | locality | 55 | Raw | n/a (descriptive) | Composition indicator (descriptive) | Phase 7B | 3 excluded | Direct measurement | Recyclability potential/prevalence | NOT a recovery measure |
| PP % | Polypropylene share | % | locality | 55 | Raw | n/a (descriptive) | Composition indicator (descriptive) | Phase 7B | 3 excluded | Direct measurement | E-commerce packaging context | NOT scored good/bad |
| HDPE/LDPE % | Combined polyethylene share | % | locality | 55 | Raw | n/a (descriptive) | Composition indicator (descriptive) | Phase 7B | 3 excluded | Direct measurement | Dominant resin category | Descriptive only |
| PS % | Polystyrene share | % | locality | 55 | Raw | n/a (descriptive) | Composition indicator (descriptive) | Phase 7B | 3 excluded | Direct measurement | Minor category | Descriptive only |
| PVC % | Polyvinyl chloride share | % | locality | 55 | Raw | Higher=higher problematic burden | Scored (problematic-material) | Phase 7B | 3 excluded | Direct measurement | Problematic-material indicator | Method-sensitive under robustness testing |
| Others % | Residual/unclassified resin share | % | locality | 55 | Raw | n/a (descriptive) | Composition indicator (descriptive) | Phase 7B | 3 excluded | Direct measurement | Residual category | Descriptive only |

## Layer B: City plastic processing performance (Phase 7C)

| Variable | Definition | Unit | Obs. level | N | Raw/Derived | Role | Source | Calculation | Limitation |
|---|---|---|---|---|---|---|---|---|---|
| Estimated generation | City-scale plastic waste generated | TPD | city | 2 | Raw | Performance indicator | Phase 7C | Direct estimate | 2 time points; no trend |
| Processed | City-scale plastic waste processed | TPD | city | 2 | Raw | Performance indicator | Phase 7C | Direct estimate | 2 time points; no trend |
| Processing gap | Generation minus processed | TPD | city | 2 | Derived | Performance indicator | Phase 7C | generation-processed | Not disaggregated by resin/fate |
| Processing efficiency | Processed/generation | % | city | 2 | Derived | Performance indicator (NOT a composite index) | Phase 7C | processed/generation x100 | N=2; no significance test applicable |

## Layer C: WTE infrastructure performance (Phase 7D)

| Variable | Definition | Unit | Obs. level | N | Raw/Derived | Role | Source | Calculation | Limitation |
|---|---|---|---|---|---|---|---|---|---|
| Designed capacity | Engineered facility capacity | TPD | facility | 4 | Raw | Context | Phase 7D | Direct record | tbp in tables |
| Processing volume | Actual reported processing | TPD | facility | 4 | Raw | Context | Phase 7D | Direct record | tbp in tables |
| Utilization % | Processing/designed capacity | % | facility | 4 | Derived | Performance indicator | Phase 7D | processing/capacity x100 | Census, not sampled; single time-period snapshot |
| Classification | Underutilized/Optimal/High Utilization/Over-Stressed | categorical | facility | 4 | Derived | Classification | Phase 7D | 4-band threshold scheme | Benchmark-dependent |
| Headroom to 85% | Additional TPD to reach 85% of capacity | TPD | facility | 2 (underutilized only) | Derived | Scenario input | Phase 7D | (85%-util%)xcapacity | Benchmark-relative, not 100%-capacity headroom |

## Layer D: Spatial context (Phase 7A/7C)

| Variable | Definition | Unit | Obs. level | N | Raw/Derived | Role | Source | Limitation |
|---|---|---|---|---|---|---|---|---|
| Zone | Administrative zone | categorical | locality | varies | Raw | Context variable | Phase 7A | Coverage varies by locality |
| Ward | MCD ward | categorical | locality | varies | Raw | Context variable | Phase 7A | Coverage varies by locality |
| Land use | Land-use classification | categorical | locality | varies | Raw | Context variable | Phase 7A | Coverage varies by locality |
| Local Moran's I | Local indicator of spatial association | numeric | locality | subset with valid spatial linkage | Derived | Scenario/context output | Phase 7C | Reported only where valid |
| Cluster classification | Hotspot/outlier/not significant | categorical | locality | subset with valid spatial linkage | Derived | Context variable | Phase 7C | Absence != low burden |

## Robustness layer (Phase 7E)

| Variable | Definition | Unit | Obs. level | N | Raw/Derived | Role | Source |
|---|---|---|---|---|---|---|---|
| Scenario | Alternative methodological specification | categorical | scenario | 69 | Raw | Robustness input | Phase 7E |
| Mean rank | Average locality rank across scenarios | numeric | locality | 55 | Derived | Performance indicator | Phase 7E |
| Rank SD | SD of locality rank across scenarios | numeric | locality | 55 | Derived | Scenario output | Phase 7E |
| Top-10 survival % | Share of scenarios with locality in top-10 | % | locality | 55 | Derived | Scenario output | Phase 7E |
| Spearman rho | Rank correlation, baseline vs. scenario | numeric | scenario-pair | 69 | Derived | Scenario output | Phase 7E |
| LOO rank displacement | Absolute rank change on removal | positions | locality | 55 | Derived | Scenario output | Phase 7E |
| Robustness class | GREEN/AMBER/RED | categorical | locality | 55 | Derived | Classification | Phase 7E |

## Institutional/EPR context layer (external, Tier 1/Tier 2)

| Variable | Definition | Role | Source |
|---|---|---|---|
| EPR recycling target (%) | Year-wise mandated recycling target for plastic packaging | Context variable | cpcb_pwm_amendment_2022, pib_epr_targets_2025 |
| National recycled tonnage | Cumulative plastic packaging recycled nationally since 2022 | Context variable (NOT locality-disaggregable) | dte_epr_recycled_2026 |
| CPCB show-cause notices | Enforcement actions against non-compliant producers | Context variable | pib_plastic_waste_2025 |

## Terminology conventions

- "Delhi NCT study area" = sampled localities, WTE facilities, MCD spatial units analyzed empirically.
- "Delhi-NCR policy context" = broader regional discussion; not empirically sampled here.
- PET, PP, HDPE/LDPE, PS, Others = descriptive composition indicators, never scored circularity components.
- PVC = scored problematic-material indicator (higher = higher problematic burden), validated only where robustness testing supports it.
- "Headroom to 85%" always means headroom relative to the 85% benchmark, never unconstrained spare capacity to 100%.
- Robustness classification (GREEN/AMBER/RED) always follows Section 4 (Analytical Framework).
