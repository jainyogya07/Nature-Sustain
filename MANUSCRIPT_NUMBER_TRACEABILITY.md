# MANUSCRIPT_NUMBER_TRACEABILITY.md

Every major manuscript number, traced: NUMBER -> SOURCE DATASET -> CALCULATION -> OUTPUT FILE -> VALIDATION -> TABLE/FIGURE -> TEXT LOCATION.

## Sampling and completeness

**58** (sampled localities) -> Phase 7A locality frame -> raw count -> Phase 7A master list -> cross-check vs. 55+3 -> Table 1 -> Sec. 3

**55** (complete resin cases) -> Phase 7A/7B -> count of non-missing across 6 resin categories -> Phase 7B complete-case file -> 58-3=55 -> Table 1, 2 -> Sec. 3, 5.1, 5.2

**3** (excluded localities, incl. Kamla Nehru Ridge) -> Phase 7A/7B exclusion log -> count missing resin data -> Phase 7B exclusion log -> 58-55=3 -> Table 1 -> Sec. 3, 5.1

**30.49%** (Kamla Nehru Ridge, raw, excluded) -> Phase 7A raw locality output -> max raw plastic % among excluded set -> Phase 7A raw file -> confirmed excluded from Phase 7B complete-case file -> Table 1 -> Sec. 3, 5.1, 6.2, Conclusion

**30.25%** (Kashmere Gate ISBT, validated max) -> Phase 7B complete-case output -> max plastic % within N=55 -> Phase 7B -> cross-check vs. Phase 7E robustness input -> Table 1, 2 -> Sec. 5.2, Abstract, Conclusion

## Locality burden scores

**1.000** (Kashmere Gate ISBT burden score) -> Phase 7B -> value/max value normalization -> Phase 7B -> Table 2 -> Sec 5.2

**0.948 / 0.807 / 0.723 / 0.672** (CBD Karkardooma / Shakarpur / Chanakyapuri / Patel Nagar) -> Phase 7B -> locality %/max % -> Phase 7B -> cross-check vs Phase 7E -> Table 2, 3 -> Sec 5.2, 5.3

**15.43%** (DAV School, max PVC) -> Phase 7B resin output -> max PVC % across N=55 -> Phase 7B -> flagged influential in Phase 7E LOO -> Table 1, 2 -> Sec 5.2, 5.6

## Resin composition means

**HDPE/LDPE=52.15%, PET=24.27%, Others=14.50%, PS=5.12%, PP=2.31%, PVC=1.65%** -> Phase 7B resin output -> arithmetic mean per category across N=55 -> Phase 7B summary -> sums to ~100% -> Table 1, 2 -> Sec 5.2, Abstract, Conclusion

## City processing

**1,117 TPD** (generation) -> Phase 7C -> reported/estimated, N=2 -> Phase 7C -> processed+gap=generation (858+259=1117) -> Table 4 -> Sec 5.4

**858 TPD** (processed) -> Phase 7C -> reported/estimated, N=2 -> Phase 7C -> generation-gap=processed -> Table 4 -> Sec 5.4

**259 TPD** (gap) -> Phase 7C -> generation-processed -> Phase 7C -> arithmetic identity -> Table 4 -> Sec 5.4

**76.81%** (efficiency) -> Phase 7C -> processed/generation x100 (858/1117) -> Phase 7C -> recomputation -> Table 4 -> Abstract, Sec 5.4, Conclusion

**8.19 pp** (gap to 85%) -> Phase 7C -> 85-76.81 -> Phase 7C -> arithmetic -> Table 4 -> Sec 5.4

**N=2** (time points) -> Phase 7C -> observation count -> Phase 7C -> row count -> Sec 3, 4, 5.4, 6.4

## WTE infrastructure

**58.3% / 68.0% / 95.8% / 108.4%** (Ghazipur/Tehkhand/Okhla/Bawana utilization) -> Phase 7D -> processing/designed capacity x100 -> Phase 7D -> cross-check vs. facility records -> Table 5 -> Sec 5.5, Abstract

**50.1 pp** (range) -> Phase 7D -> 108.4-58.3 -> Phase 7D -> arithmetic -> Table 5 -> Sec 5.5

**28.3%** (CV) -> Phase 7D -> SD/mean of 4 values x100 -> Phase 7D -> recomputation -> Table 5 -> Sec 5.5

**347.7 TPD** (Ghazipur headroom to 85%) -> Phase 7D -> (85%-58.3%)xcapacity -> Phase 7D -> cross-check vs. combined figure -> Table 5 -> Sec 5.5

**340.7 TPD** (Tehkhand headroom to 85%) -> Phase 7D -> (85%-68.0%)xcapacity -> Phase 7D -> cross-check -> Table 5 -> Sec 5.5

**688.4 TPD** (combined headroom) -> Phase 7D -> 347.7+340.7 -> Phase 7D -> arithmetic identity -> Table 5 -> Sec 5.5, 5.7, 6.5

## Robustness

**69** (scenarios) -> Phase 7E -> count of specification combinations -> Phase 7E scenario log -> scenario-count cross-check -> Table 6 -> Sec 4, 5.6

**0.900** (mean Spearman rho) -> Phase 7E -> mean of rank correlations across 69 scenarios -> Phase 7E summary -> cross-check -> Table 6 -> Abstract, Sec 5.6

**83.3%** (mean Top-10 overlap) -> Phase 7E -> mean overlap of top-10 lists across scenarios -> Phase 7E summary -> cross-check -> Table 6 -> Abstract, Sec 5.6

**0.57** (mean LOO rank displacement) -> Phase 7E -> mean absolute rank change under LOO -> Phase 7E LOO output -> cross-check -> Table 6 -> Abstract, Sec 5.6

**5** (robust GREEN priorities) -> Phase 7E -> count of GREEN-classified localities -> Phase 7E classification output -> cross-check vs Table 6 -> Table 6, 8 -> Sec 5.6, Conclusion

**DAV School, Kashmere Gate ISBT** (influential observations) -> Phase 7E LOO output -> identification of disproportionate LOO effect -> Phase 7E LOO output -> cross-check vs Table 2 -> Table 2, 6 -> Sec 5.6, 6.6

## External reference figures (context only, not merged with internal numbers)

**~63% total-MSW processed, ~4,200 TPD total-MSW gap, ~11,862 TPD total-MSW generation** -> Delhi Economic Survey 2025-26 -> official reporting -> delhi_eco_survey_2026 -> independently reported, different denominator than plastic-specific figures -> Table 4 (context row) -> Sec 5.4, 6.1, 6.4

**108 shutdown-days (Ghazipur, FY2025-26)** -> Hindustan Times, Jan 2026 -> reported operational status -> ht_ghazipur_shutdown_2026 -> news reporting, Tier 3, used for corroborating context only -> Table 5 (context) -> Sec 5.5, 6.5

**CPCB compliance affidavit findings (Bawana dioxin/furan; Ghazipur/Tehkhand effluent; Okhla compliant)** -> CPCB affidavit before NGT, reported Feb 2026 -> official compliance finding -> ht_cpcb_affidavit_2026 -> Tier 1-adjacent (CPCB-sourced, reported via news) -> Table 5 (context) -> Sec 5.5, 6.5

**20.7 million tonnes plastic packaging recycled since 2022** -> PIB/Down To Earth, March 2026 -> national EPR reporting -> dte_epr_recycled_2026 -> national aggregate, not locality-disaggregable -> Sec 5.2, 6.3

## Outstanding items pending validated output

SD/min for all resin-category means (Table 1); full 55-locality listing (Table 2); zone/ward/land-use/Moran's I/p-values for all localities (Table 3); designed capacity and absolute processing tonnage per facility (Table 5); full 69-scenario, 55-locality robustness table (Table 6); distance/cost figures for diversion pathways (Table 7). These are marked "tbp" (to be populated) throughout and must be filled only from validated Phase 7 output files, never invented.
