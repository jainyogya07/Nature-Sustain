# All tables from the manuscript

Exact wording from `main.tex`, in the order they appear in the paper.

---

## Table 1. Evidence streams used in urban plastic-waste decisions and the transfer boundary between them

**Label:** `tab:litstream`

| Evidence stream | What it measures | What it can support | What it cannot support | Transfer condition |
|---|---|---|---|---|
| Global plastic mass (Geyer et al., 2017; Jambeck et al., 2015; Cook et al., 2025) | Planetary production, leakage, treatment lag | A public statement of magnitude | A neighbourhood, resin, or plant assignment | Local measurement of the object to be moved |
| Circular-economy constructs (Kirchherr et al., 2017; Geissdoerfer et al., 2017; Hossain et al., 2022) | Circularity as an umbrella; source-specific recovery as the Indian weakness | Policy framing; identification of a recovery gap | A Delhi NCT locality at which EPR can be audited | Capture measurement at the named site |
| Composition surveys (CPCB, 2015; Directorate of Environment, NCT of Delhi, 2019; CPCB, 2024) | Resin prevalence by city or area type | Material-specific investigation; PET/PVC site flags | Recovery, recycling rate, or circularity | Capture/recovery measurement required |
| Spatial association (Anselin, 1995; Getis & Ord, 1992; Kumar, Choudhary & Mathur, 2026) | Local association (LISA / Gi*) | Zone-level intervention where *p*<0.05 | Isolated-site cause; high-burden as hotspot | Local statistic at the decision unit |
| City processing ledgers (Sharholy et al., 2008; Talyan et al., 2008; Delhi Economic Survey, 2026) | City-scale processed/generated ratio | System monitoring; a ledger warning | Plant capacity or a named bottleneck | Facility-level utilization data |
| WTE / plant operations (DPCC, 2025; Astrup et al., 2015; Hindustan Times CPCB affidavit, 2026) | Facility utilization, downtime, compliance flags | Candidate sink; blocked node; operational relief | Route allocation; proven emissions cause | Network, availability, and compliance files |
| Rank robustness (Belton & Stewart, 2002; Saltelli et al., 2008) | Stability of a priority ordering under specification change | Provisional targeting of surviving names | A guaranteed programme from an untested list | Specification test before spend |
| Reverse logistics (Fleischmann et al., 1997; Govindan et al., 2015; Das & Bhattacharyya, 2015) | Origins, sinks, and capacities as constraints | A feasibility file for later routing | An optimal vehicle route | Observed roads, fleet, time windows, costs |

**Note.** The table maps existing streams. It does not claim this is the first Delhi plastic-waste paper. How those streams are joined is shown in the final synthesis after the results.

---

## Table 2. Data provenance: evidence objects kept on separate ledgers

**Label:** `tab:provenance`

| Evidence | Unit | Period | N | Source | Role | Main limitation |
|---|---|---|---|---|---|---|
| Plastic burden and resin mix | Locality | Compiled complete-resin file | 58 | Locality composition file | Object A: burden and prevalence | Complete-case frame, not a probability sample; four sites <10 kg |
| Spatial association | Locality (coordinates) | Same frame | 58 | Local Moran's I file | Object B: cluster vs isolated peak | Exploratory site-wise *p*; no FDR; unclassified ≠ low burden |
| City plastic ledger | Delhi NCT | March and June 2025 | 2 | DPCC MPR Section VIII (DPCC, 2025) | Object C: processed/generated ratio | Two records; no interval; no trend |
| WTE utilization | Facility | March 2025 census | 4 | DPCC MPR Annexure-5 (DPCC, 2025) | Object D: utilization class and mixed-waste headroom | Snapshot, not continuous availability; mixed-waste, not plastic |
| Priority stability | Locality rank | Specification registry | 72 rows | Robustness file | Object E: GREEN/AMBER/RED gate | Gate, not a score; mean ρ does not licence every name |
| Diversion feasibility | Origin–sink pair | Scenario, not a timetable | -- | Utilization classes + GREEN demand | Object F: constraint set | No GPS, fleet, time windows, or costs |

**Note.** Objects are linked sequentially, not averaged. External reports (Economic Survey, CPCB affidavit, shutdown coverage) are context, convergence, or contrast and never override these files.

---

## Table 3. Empirical data coverage and material-composition baseline

**Label:** `tab:table1`

| Variable | Obs. level | N | Mean | SD | Min | Max | Unit | Data source | Analytical role |
|---|---|---|---|---|---|---|---|---|---|
| Sampled localities | Locality | 58 | -- | -- | -- | -- | count | Locality composition file | Complete-case frame, not a census |
| Complete resin cases | Locality | 58 | -- | -- | -- | -- | count | Locality composition file | Basis for composition analysis |
| Small-sample flag (<10 kg) | Locality | 4 | -- | -- | -- | -- | count | Field sample mass | Ridge, DAV School, CBD Karkardooma, Ryan International; retained, not dropped |
| Plastic % | Locality | 58 | 10.82 | 6.10 | 1.98 (Okhla Mandi) | 30.49 (Kamla Nehru Ridge) | % | Locality composition file | Basis for burden score |
| PET % | Locality | 58 | 23.60 | 20.27 | 0.95 | 100.00 (Akshardham Temple) | % | Locality composition file | Descriptive composition indicator |
| PP % | Locality | 58 | 2.79 | 6.54 | 0.00 | 34.67 (Kamla Nehru Ridge) | % | Locality composition file | Descriptive composition indicator |
| HDPE/LDPE % | Locality | 58 | 53.24 | 24.49 | 0.00 | 95.28 (Shakarpur) | % | Locality composition file | Descriptive composition indicator |
| PS % | Locality | 58 | 4.92 | 6.69 | 0.00 | 36.45 (Ryan International) | % | Locality composition file | Descriptive composition indicator |
| PVC % | Locality | 58 | 1.65 | 2.41 | 0.00 | 15.43 (DAV School) | % | Locality composition file | Scored problematic-material indicator |
| Others % | Locality | 58 | 13.80 | 13.17 | 0.00 | 45.63 (Chanakyapuri) | % | Locality composition file | Residual descriptive category |

**Note.** Burden score is plastic % divided by the sample maximum (Kamla Nehru Ridge = 30.49% = 1.000). It is a relative index inside this *N*=58 frame, not an absolute environmental-risk score. PET and PP are descriptive composition indicators; PVC is a scored problematic-material indicator. Four sites have sample mass below 10 kg and are flagged in the text. The 58 names are the complete-resin cases in the locality composition file, not a probability sample of Delhi NCT.

---

## Table 4. Terminology used for each evidence layer

**Label:** `tab:terminology`

| Term | Meaning as used in this manuscript |
|---|---|
| Plastic burden indicator (scored) | Locality plastic % and its 0–1 normalized burden score (Kamla Nehru Ridge = 1.000 within *N*=58). |
| PVC problematic-material indicator (scored) | Locality PVC %; higher values indicate higher problematic-material burden, scored only where the underlying data are validated. |
| PET composition indicator (descriptive) | Locality PET %, read as PET prevalence relevant to recovery assessment, never as realized recycling, material quality, or collection efficiency, and never scored as a circularity outcome. |
| PP composition indicator (descriptive) | Locality PP %, read as packaging prevalence context. E-commerce relevance is interpretive, not directly measured, and PP is not scored as a performance outcome. |
| HDPE/LDPE, PS, Others (descriptive) | Compositional shares reported for completeness; not independently scored. |
| City plastic processing performance indicator | Processed/generated plastic tonnage ratio at Delhi NCT scale (two recorded TPD figures); a ledger ratio, not a statistical estimate. |
| WTE infrastructure utilization | Processed/designed-capacity ratio per facility (4 facilities; March 2025 census snapshot). |
| Spatial context | Zone, ward, land use, and local cluster classification per locality, confined to the Delhi NCT study area. |
| Robust intervention priority | A locality whose recorded class is GREEN (Section 5.4). Immediate collection spend is licensed only for those names. Robustness is a gate and a classification, not an additional score. |
| Typed intervention licence | A decision permission whose spatial and operational scope matches the evidence object that supports it: site, zone, facility, city investigation, or later optimization (Table 6). |
| Evidence-scale mismatch | Use of an observation generated at one analytical unit, geographic extent, temporal window, denominator, or system boundary to justify a decision at another level without demonstrating that the inference is transferable (Table 5). |
| Licensed intervention | An action that operates at the same decision scale as the supporting evidence, states its uncertainty, and does not require an unmeasured causal or operational assumption (Table 6). |

---

## Table 5. Five forms of evidence-scale mismatch

**Label:** `tab:mismatch`

| Form | What is transferred without warrant | Delhi NCT illustration in this study |
|---|---|---|
| Spatial mismatch | Locality evidence used to make citywide or NCR-wide claims | *N*=58 complete-resin localities are not a probability sample of NCT neighbourhoods and not a census of MCD wards; Delhi-NCR is not sampled |
| Temporal mismatch | A two-time-point processing estimate used to imply a long-term trend | DPCC Section VIII records 1,117 TPD generated and 858 TPD processed in March and June 2025; *N*=2, no interval, no trend |
| Material mismatch | PET/PP composition used as evidence of actual material recovery | Mean PET 23.60% is prevalence relevant to recovery assessment, not locality PET capture |
| System-boundary mismatch | Plastic-specific processing compared directly with total-MSW processing | 76.81% plastic processed (858/1,117) is a different denominator from ≈63% total MSW processed |
| Operational mismatch | WTE utilization or benchmark headroom treated as immediate routing capacity or optimized flow allocation | Combined mixed-waste headroom of 688.4 TPD is not plastic-only capacity, not continuous availability, and not a solved route |

---

## Table 6. Evidence, licensed intervention, and the claim the evidence does not support

**Label:** `tab:licensed`

| Evidence | Licensed intervention | Not licensed |
|---|---|---|
| High locality plastic burden (Ridge 30.49%; Kashmere Gate ISBT 30.25%; CBD Karkardooma 22.68%) | Enhanced collection and segregation assessment at surviving GREEN names | Claiming citywide processing failure from locality shares |
| High PET composition (mean 23.60%; Kashmere Gate ISBT 83.68%) | MRF access and recovery audit where PET is prevalent | Claiming high PET circularity or locality recovery |
| High PVC at DAV School (15.43%) | Site-level material investigation | Citywide PVC restriction |
| Underutilized Ghazipur (58.3%) and Tehkhand (68.0%) | Feasibility assessment for diversion up to mixed-waste headroom | Immediate guaranteed diversion allocation or a solved route |
| Bawana at 108.4% utilization | Operational-relief assessment; keep Okhla (95.8%) as High Utilization, not slack | Claiming a proven cause of emissions non-compliance |
| Robust top locality rank (three of 58 names; ρ=0.893) | Priority field intervention at Ridge, Kashmere Gate ISBT, and CBD Karkardooma | Claiming a causal explanation for their burden, or treating untested ranks as a programme |

**Note.** An intervention is evidence-licensed only when the action operates at the same decision scale as the supporting evidence, uncertainty is stated, and no unmeasured causal or operational assumption is required. Read with the mismatch typology. The later intervention screen applies the same rule.

---

## Table 7. Robustness tests and the intervention each one can affect

**Label:** `tab:robusttests`

| Test | What it protects against | Intervention affected |
|---|---|---|
| Appearance stability (≥8/9 top-10 tests) | Whether the locality remains in the recorded top-10 when weights and scaling change | Site-priority licence (GREEN if also not LOO-influential) |
| Leave-one-out influence (mean displacement of remaining ranks >1.0) | Effect of removing a locality on the ranking of the remaining localities | Multi-site programme; not a bar to site collection at a non-influencer |

**Note.** Kashmere Gate ISBT is GREEN: 8/9 appearance and mean leave-one-out displacement 0.96 (maximum 1). DAV School is AMBER: 9/9 appearance but mean displacement 3.7 (maximum 19). The threshold mean >1.0 is the registry rule used to flag influential removals.

---

## Table 8. What the data establish and do not establish

**Label:** `box:cancannot`

| Established by this study | Not established by this study |
|---|---|
| Locality-level plastic burden (*N*=58) | Locality-level PET recovery rate |
| Resin composition by category (*N*=58) | Locality-level PP recovery rate |
| Spatial variation across sampled Delhi NCT localities; LISA hotspots where *p*<0.05 | Causal effect of land use on plastic burden; citywide hotspot map for unclassified points |
| City-level plastic processing ratio (two recorded TPD figures; no interval) | Causal impact of EPR enforcement on Delhi outcomes |
| WTE facility utilization differences (4 facilities, census) | Complete Delhi-NCR coverage |
| Robustness of priority rankings (appearance-rate and LOO tests) | Continuous WTE plant availability from one utilization estimate |
| Benchmark-based facility headroom scenarios | Mathematically optimal vehicle routes |

---

## Table 9. Locality-level plastic burden and resin composition (*N*=58; selected localities shown)

**Label:** `tab:table2`

| Locality | Plastic % | Burden score | PVC % | PET % | PP % | HDPE/ LDPE % | PS % | Others % | Robustness |
|---|---|---|---|---|---|---|---|---|---|
| Kamla Nehru Ridge | 30.49 | 1.000 | 0.00 | 6.67 | 34.67 | 58.67 | 0.00 | 0.00 | GREEN (small sample) |
| Kashmere Gate ISBT | 30.25 | 0.992 | 0.00 | 83.68 | 0.00 | 9.30 | 0.00 | 7.02 | GREEN |
| CBD Karkardooma | 22.68 | 0.744 | 0.00 | 38.58 | 0.00 | 30.71 | 16.54 | 14.17 | GREEN (small sample) |
| National Museum | 19.51 | 0.640 | 0.00 | 52.10 | 0.00 | 47.90 | 0.00 | 0.00 | AMBER |
| Ryan International School | 19.11 | 0.627 | 0.00 | 19.63 | 0.00 | 43.93 | 36.45 | 0.00 | RED |
| DAV School | 17.24 | 0.565 | 15.43 | 14.04 | 16.01 | 41.76 | 12.76 | 0.00 | AMBER (LOO influential) |
| Shakarpur | 17.10 | 0.561 | 0.80 | 0.95 | 0.00 | 95.28 | 2.17 | 0.80 | AMBER |
| Remaining 51 of 58 localities: same composition file; ranked list not reprinted here. | | | | | | | | | |

**Note.** Burden score = plastic % / 30.49. PVC is scored; PET, PP, HDPE/LDPE, PS, and Others are descriptive. Small-sample sites (<10 kg): Ridge, DAV School, CBD Karkardooma, Ryan International. Robustness categories are assigned in the later robustness registry.

---

## Table 10. Spatial heterogeneity and locality-level priority evidence

**Label:** `tab:table3`

| Locality | Ward | Zone | Land use | Plastic burden | Spatial statistic (local Moran's I) | p | Cluster class. | Interpretation |
|---|---|---|---|---|---|---|---|---|
| Kamla Nagar Market | 69 | North | Commercial | 15.00 | 2.183 | 0.002 | High–high | Strong hotspot |
| Tis Hazari Court | 83 | North | Institutional | 11.53 | 0.119 | 0.028 | High–high | Strong hotspot |
| Madanpur Khadar | 101-S | South East | Residential | 5.30 | 0.949 | 0.006 | Low–low | Strong coldspot |
| Dwarka Sector-12 | 36 & 38 | Dwarka | Residential | 9.27 | 0.228 | 0.028 | Low–low | Strong coldspot |
| Civil Lines | 83 | North | Residential | 6.75 | −2.157 | 0.040 | Low–high | Spatial outlier |
| Nizamuddin Railway Station | -- | South East | Public | 11.13 | −0.060 | 0.040 | High–low | Spatial outlier |
| Kamla Nehru Ridge | Ridge | Central | Mixed | 30.49 | -- | -- | Not classified | Highest burden; not a LISA hotspot |
| Kashmere Gate ISBT | -- | North | Public | 30.25 | -- | -- | Not classified | Isolated high-burden generator |

**Note.** Spatial weights: *k*=5 nearest neighbours (Haversine km), inverse-distance among those neighbours, row-standardized. Local Moran's I from 999 conditional permutations; site-wise *p*<0.05 labelled strong. No false-discovery correction is applied across the 58 local tests; classifications are exploratory. Ajmal Khan Road Market is a marginal high–high cluster (*p*=0.066) and is not treated as confirmed. High-burden GREEN sites without a LISA label are isolated generators, not hotspots. Method follows ward-level MSW hotspot analysis in Kumar, Choudhary and Mathur (2026), adapted to locality plastic burden. Delhi NCT sample only.

---

## Table 11. Delhi NCT plastic processing performance

**Label:** `tab:table4`

| Metric | Value | Unit | Benchmark | Difference | Evidence source | Interpretation |
|---|---|---|---|---|---|---|
| Estimated generation | 1,117 | TPD | -- | -- | DPCC MPR, March and June 2025, Section VIII (DPCC, 2025) | Identical in both months |
| Processed | 858 | TPD | -- | -- | DPCC MPR, March and June 2025, Section VIII (DPCC, 2025) | Identical in both months |
| Processing gap | 259 | TPD | -- | -- | 1,117−858 | Arithmetic processing remainder; not disaggregated by resin/fate; not additive to total-MSW gap |
| Processing efficiency | 76.81 | % | 85% (operating band) | ≈8 pp | 858/1,117 | Exact quotient of two records; no interval; not a composite index |
| Context only, different denominator: total-MSW gap ≈4,200 TPD on ≈11,862 TPD generated, ≈63% processed (Delhi Economic Survey, 2026) | | | | | | |

**Note.** Two recorded TPD figures from DPCC monthly progress reports, Section VIII (Plastic Waste Management), March 2025 and June 2025 (DPCC, 2025). These city plastic quantities are not taken from Annexure-5, which is the four-plant mixed-waste census. The 76.81% figure is 858/1,117 to two decimals. It is not a statistical estimate and has no confidence interval. TPD = tonnes per day. The 85% figure is the study-defined operating-band reference in Section 4, not a regulatory target. The 259 TPD arithmetic processing remainder is not a documented destination.

---

## Table 12. WTE facility utilization and benchmark classification

**Label:** `tab:table5`

| Facility | Designed capacity | Processing | Util. % | Classification | Mixed-waste headroom to 85% | Operational interpretation |
|---|---|---|---|---|---|---|
| Ghazipur | 1,300 | 757.3 | 58.3 | Underutilized | 347.7 TPD | Direction matches reported 108-day FY2025-26 shutdown (Hindustan Times, 2026) |
| Tehkhand | 2,000 | 1,359.3 | 68.0 | Underutilized | 340.7 TPD | CPCB affidavit flags effluent-treatment lapses (Hindustan Times, 2026) |
| Okhla | 1,950 | 1,867.9 | 95.8 | High Utilization | -- | Not over-stressed; only plant meeting all monitored CPCB norms (Hindustan Times, 2026) |
| Bawana | 2,000 | 2,167.5 | 108.4 | Over-Stressed | -- | Above designed capacity; CPCB affidavit flags dioxin/furan exceedances |
| Utilization range = 50.1 pp (heterogeneity metric); CV = 28.3%; combined Ghazipur+Tehkhand mixed-waste throughput headroom to 85% = 688.4 TPD | | | | | | |

**Note.** Bands: <85% Underutilized; 85–95% Optimal; 95–100% High Utilization (conditionally admissible, not slack); >100% Over-Stressed. Source: DPCC (2025), Annexure-5 (facility mixed-waste census snapshot). Headroom is mixed-waste throughput to the 85% operating band, not plastic-only capacity. External reports are directional context.

---

## Table 13. Robustness of locality intervention priorities (appearance-rate registry)

**Label:** `tab:table6`

| Locality | Top-10 hits | Survival % | LOO influence | Class |
|---|---|---|---|---|
| Kamla Nehru Ridge | 8/9 | 88.9 | 0.98 (max 2) | GREEN |
| Kashmere Gate ISBT | 8/9 | 88.9 | 0.96 (max 1) | GREEN |
| CBD Karkardooma | 8/9 | 88.9 | 0.95 (max 1) | GREEN |
| DAV School | 9/9 | 100.0 | 3.74 (max 19) | AMBER |
| National Museum | 7/9 | 77.8 | -- | AMBER |
| Shakarpur | 6/9 | 66.7 | -- | AMBER |
| Ryan International School | 5/9 | 55.6 | -- | RED |
| Weighting mean Spearman ρ=0.893; mean top-10 overlap=83.3%; mean LOO displacement=0.55; 3 GREEN | | | | |

**Note.** Hits are appearances in the recorded top-10 test (9 weighting/normalization rows). LOO influence is mean (maximum) rank displacement of the remaining localities when that name is removed. Influence is flagged when that mean exceeds 1.0; only DAV School meets that rule. GREEN/AMBER/RED are locality-priority classes only (Table 7). Three of 58 names are GREEN.

---

## Table 14. Reverse-logistics constraint set (not a routing solution)

**Label:** `tab:table7`

| Illustrative origin | Role in the set | Permitted sink | Assumed extra km | Mixed-waste headroom to 85% |
|---|---|---|---|---|
| Dwarka Sector-12 | Demand node (scenario) | Tehkhand | 1.2 | 340.7 TPD |
| Azadpur Mandi | Demand node (scenario) | Ghazipur | 1.9 | 347.7 TPD |
| Vikaspuri | Demand node (scenario) | Tehkhand | 3.39 | 340.7 TPD |
| Uttam Nagar | Demand node (scenario) | Tehkhand | 3.39 | 340.7 TPD |
| Burari Sant Nagar | Demand node (scenario) | Ghazipur | 3.57 | 347.7 TPD |
| Bawana (facility) | Blocked node (108.4% observed) | --- | --- | Load withheld |
| Okhla (facility) | High Utilization (95.8%) | --- | --- | Not treated as slack |

**Note.** Origins are scenario demand nodes; extra km are assumed round-trips. Sink headroom is mixed-waste throughput to the 85% operating band from DPCC (2025), Annexure-5; it is not the city plastic remainder of 259 TPD in Table 11. Direction matches MCD capacity notices (New Indian Express, 2025; Times of India, 2026).

---

## Table 15. Evidence-to-intervention decision table

**Label:** `tab:table8`

| Evidence object | Finding | Evidence status | Licensed intervention | Explicitly not licensed |
|---|---|---|---|---|
| Material burden | Up to 30.49% (*N*=58); Ridge 30.49%, Kashmere Gate 30.25%, CBD 22.68% | ROBUST PRIORITY | Collection/segregation at robust high-burden sites, with small-sample flags | Citywide processing failure from locality shares |
| PVC | Max 15.43% (DAV School); mean 1.65% | INVESTIGATION | Site-specific PVC investigation | Citywide PVC restriction or a PET recycling rate analogue |
| PET | Mean 23.60%; Kashmere Gate 83.68% | DESCRIPTIVE | MRF access/throughput and capture assessment | PET recycling rate or locality circularity |
| PP | Mean 2.79% | DESCRIPTIVE | EPR-linked recovery-pathway assessment | E-commerce origin or a performance score |
| Processing ledger | 858 of 1,117 TPD; remainder 259 TPD | TWO-RECORD LEDGER | Plastic fate/ledger investigation | Citywide recycling-efficiency claim or a trend |
| WTE utilization | 58.3–108.4%; 50.1 pp range | CENSUS SNAPSHOT | Scenario-based load rebalancing: fill Ghazipur/Tehkhand; relieve Bawana | Optimal routing; treating Okhla as slack |
| Bawana over-stress | 108.4% of design | CENSUS SNAPSHOT | Operational-relief assessment | Proven cause of emissions non-compliance |
| Spatial concentration | High–high: Kamla Nagar Market, Tis Hazari; Ridge and Kashmere Gate not classified | LISA-CONFIRMED | Zone plans for confirmed hotspots; site lifting at isolated generators | High-burden name as hotspot name |

**Note.** Evidence status names the type of supporting object. GREEN/AMBER/RED are reserved for locality-priority classes (Tables 7 and 13) and are not reused as chips for plants, ledgers, or clusters. Read with Table 6.

---

## Figure 8 (tabular decision screen in the manuscript)

**Label:** `fig:fig8`

**Caption.** Evidence-to-intervention decision screen. Status chips name the evidence object. Corresponds to Table 15. Do not transfer evidence beyond its measurement scale without validation.

| Evidence object | Evidence status | Licensed | Not licensed |
|---|---|---|---|
| 1. Locality burden | ROBUST PRIORITY | Collection at Ridge, Kashmere Gate, CBD | Export of these ranks to other cities or years |
| 2. PVC | INVESTIGATION | Site investigation at DAV School | Citywide PVC restriction |
| 3. PET / PP | DESCRIPTIVE | MRF access and capture assessment | Equating PET share with a recycling rate |
| 4. City processing | TWO-RECORD LEDGER | Plastic line and fate investigation | Trend or forecast from *N*=2 |
| 5. WTE utilization | CENSUS SNAPSHOT | Relieve Bawana; fill Ghazipur/Tehkhand | Treating Okhla as slack |
| 6. Spatial clusters | LISA-CONFIRMED | Zone plans for confirmed clusters; site lifting at isolated generators | High-burden name as hotspot name |

**Note.** GREEN/AMBER/RED are reserved for locality-priority robustness classes (Table 13). Other labels identify the evidence type and are not robustness grades.

---

## Table 16. How disconnected literature streams are joined into an evidence-linked decision architecture

**Label:** `tab:contribution`

| Conventional sequence | Evidence unit kept separate | Diagnosis produced | Gate applied | Intervention licensed |
|---|---|---|---|---|
| Composition surveys (Directorate of Environment, NCT of Delhi, 2019; CPCB, 2015; CPCB, 2024) | Locality burden and resin mix (*N*=58) | Named tail: Ridge 30.49%, Kashmere Gate 30.25%; PET as prevalence (23.60%); PVC scored at DAV School 15.43% | Priority status varies by locality; Ridge, Kashmere Gate ISBT and CBD Karkardooma survive the robustness gate. PVC at DAV School is held AMBER (LOO) | Site lifting at GREEN generators; site inspection at DAV School, not a city PVC ban |
| Spatial MSW analysis (Kumar, Choudhary & Mathur, 2026) | Local Moran's I only where *p*<0.05 | High–high: Kamla Nagar Market, Tis Hazari; Ridge and Kashmere Gate unclassified | High-burden name ≠ hotspot name | Zone plan for confirmed clusters; site lifting for isolated generators |
| City MSW aggregates (Delhi Economic Survey, 2026; MCD SWM presentation) | Plastic ledger (two records), distinct from ≈63% total MSW | 858 of 1,117 TPD processed; 259 TPD remainder | Remainder not mixed with mixed-waste headroom | Plastic line in the municipal ledger; fate study |
| WTE technology reviews (Kalyani & Pandey, 2014; Kumar & Samadder, 2017) | Four-plant census from DPCC (2025) | 50.1 pp spread; Ghazipur/Tehkhand underused; Okhla 95.8% High Utilization; Bawana 108.4% over-stressed | Headroom kept as mixed-waste throughput; Okhla not treated as slack | Two jobs: relieve Bawana; fill Ghazipur/Tehkhand |
| Policy targeting without specification testing (Hossain et al., 2022; MoEFCC, 2026) | Policy frameworks specify obligations but do not, in the cited evidence, establish locality-level priority stability. This study introduces a specification registry (72 rows) before immediate intervention | ρ=0.893; top-10 overlap 83.3%; LOO 0.55; three of 58 names survive | Immediate spend withheld from method-sensitive names | Immediate spend only on Ridge, Kashmere Gate, CBD Karkardooma |

**Note.** Column sequence is the join demonstrated after the results. Ranks are not exported; the architecture is. Read with Tables 5, 6 and 15.
