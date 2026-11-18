# Data availability and Code availability

Journal-ready statements for *Nature Sustainability*, written to the Nature Portfolio reporting policy ([Reporting standards and availability of data, materials, code and protocols](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards); [Data availability statements guidance](https://www.nature.com/documents/nr-data-availability-statements-data-citations.pdf); [Guidelines for authors submitting code](https://www.nature.com/documents/GuidelinesCodePublication.pdf)).

**Where these go in the manuscript.** *Nature Sustainability* follows Nature Portfolio end-matter order: after Methods, as two separate headed sections, **Data availability** then **Code availability**, before Acknowledgements / References. Headings are sentence case. Do not merge them into one paragraph.

**What is and is not claimed.** File paths, row counts, and URLs below were checked against the working copy of this repository on 18 November 2026. A Zenodo DOI has **not** been minted yet; that fact is stated in Code availability rather than invented. Government source URLs that returned HTTP 200 in that check are marked **verified**. URLs taken from the manuscript bibliography that timed out in this session are marked **bibliographic**, not guessed.

---

## Data availability

The minimum dataset required to interpret, verify and extend the findings of this study is deposited in the public GitHub repository [https://github.com/jainyogya07/Nature-Sustain](https://github.com/jainyogya07/Nature-Sustain) (MIT Licence). That deposit comprises (i) the compiled *N* = 58 Delhi NCT locality composition file with table- and page-level provenance; (ii) derived locality burden and six-resin shares; (iii) local Moran’s *I* / LISA outputs; (iv) the two-record city plastic ledger extract (1,117 TPD generated, 858 TPD processed, 259 TPD remainder; 76.81%); (v) the four-plant mixed-waste utilization census extract (Ghazipur 58.3%, Tehkhand 68.0%, Okhla 95.8%, Bawana 108.4%); (vi) the 72-row specification registry and leave-one-out influence file; (vii) the reverse-logistics constraint set; and (viii) manuscript tables as CSV. Source data for Figures 1–8 are in `figures/` and the CSV files listed below.

Locality burden and resin composition were compiled from the publicly available government-commissioned report *Assessment and Characterization of Plastic Waste in NCT of Delhi* (July 2020), Shriram Institute for Industrial Research, prepared for the Department of Environment, Government of NCT of Delhi ([https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf](https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf); HTTP 200 verified 18 November 2026; PDF 4,090,547 bytes). City-scale plastic generation and processing, and the four-plant mixed-waste census, were read from Delhi Pollution Control Committee Monthly Progress Reports submitted to the National Green Tribunal: Section VIII (Plastic Waste Management) of the March 2025 and June 2025 reports (identical 1,117 / 858 TPD), and Annexure-5 of the March 2025 report (facility design capacity and throughput). The DPCC series is cited at [https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi](https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi). Mixed-MSW context figures (approximately 63% processed on a different denominator) are from the Delhi Economic Survey 2025–26, Planning Department, Government of NCT of Delhi ([https://delhiplanning.delhi.gov.in/](https://delhiplanning.delhi.gov.in/); portal HTTP 200 verified). National EPR and plastic-waste rule documents are available from the CPCB Plastic Waste Management portal ([https://pwm.cpcb.gov.in/](https://pwm.cpcb.gov.in/); HTTP 200 verified) and the CPCB EPR portal ([https://eprplastic.cpcb.gov.in/](https://eprplastic.cpcb.gov.in/); HTTP 200 verified).

Third-party government reports remain copyright of the originating agencies and are not redistributed in full. Compiled extracts sufficient to reproduce the analyses are in the repository. No confidential personal identifiers were collected. There is no embargo and no access fee. Further files, if any, are available from the corresponding author (Sonal Khurana, Vivekananda Institute of Professional Studies – Technical Campus; [sonal.khurana@gmail.com](mailto:sonal.khurana@gmail.com)) on reasonable request.

---

## Code availability

Custom Python code used to compile the locality file, compute Haversine *k* = 5 inverse-distance local Moran’s *I* with 999 conditional permutations, classify waste-to-energy utilization, run the 72-specification robustness registry, and draw manuscript figures is available at [https://github.com/jainyogya07/Nature-Sustain](https://github.com/jainyogya07/Nature-Sustain) under the MIT Licence, without embargo or registration. Principal entry points are `pipeline_v2/` (analysis) and `figures/build_figures.py` (figures). Runtime: Python ≥ 3.10; packages listed in `requirements.txt` (`pandas`, `numpy`, `scipy`, `matplotlib`).

A persistent DOI has not yet been issued. Upon acceptance, the tagged release of this repository will be archived on Zenodo so that a versioned DOI can be added to the article and cited in the reference list in Nature Portfolio / DataCite form (authors, title, repository, identifier as a full URL). Until that archive exists, the canonical access point is the GitHub repository named above. There are no licence restrictions beyond MIT, no commercial-use bar, and no requirement for co-authorship as a condition of access. Code questions: Sonal Khurana, [sonal.khurana@gmail.com](mailto:sonal.khurana@gmail.com).

---

## Verified inventory (repository objects)

These are the files that constitute the minimum dataset. Row counts are data rows, excluding the header.

### Object A: locality burden and resin composition (*N* = 58)

| File | Rows | What it is | Origin |
|---|---:|---|---|
| `pipeline_v2/locality_plastic_analysis_v2.csv` | 58 | Master compiled locality file (51 fields): SRI table/page numbers, coordinates, sample mass, plastic %, six-resin kg and % shares, complete-case flags | Author compilation from SRI 2020 tables |
| `sri_plastic_study_complete_extraction.csv` | 58 | Parallel extraction of the same SRI tables | Author compilation |
| `phase7c_locality_full_resin_composition.csv` | 58 | Location, zone, income, land use, PET / HDPE-LDPE / PVC / PP / PS / Others % | Derived from Object A |
| `phase7c_locality_plastic_burden_scores.csv` | -- | Burden score = plastic % / sample maximum (Ridge 30.49% = 1.000) | Derived |
| `phase7c_resin_composition_summary_stats.csv` | -- | Sample means used in the text (HDPE/LDPE 53.24%, PET 23.60%, Others 13.80%, PS 4.92%, PP 2.79%, PVC 1.65%) | Derived |

**Primary source (third party, public).** Shriram Institute for Industrial Research, *Assessment and Characterization of Plastic Waste in NCT of Delhi* (July 2020), commissioned by the Department of Environment, Government of NCT of Delhi. Direct PDF: [https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf](https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf) (**verified** HTTP 200, `content-type: application/pdf`, 4,090,547 bytes, last-modified 23 April 2023). The compiled CSV records `source_document`, `source_organization`, `sri_table_number` and `sri_page_number` for each row so that every locality can be traced back to a table in that PDF.

**Limitations that the paper already states.** Complete-resin frame, not a probability sample of NCT neighbourhoods and not a census of MCD wards; four sites have sample mass &lt; 10 kg and are retained with that flag (Ridge, DAV School, CBD Karkardooma, Ryan International School). Delhi-NCR satellite cities are not in the file.

### Object B: spatial association (LISA)

| File | Rows | What it is |
|---|---:|---|
| `pipeline_v2/advanced_analytics/8c_lisa_hotspots_elite.csv` | 11 | Sites with local Moran’s *I* labelled at least marginal: High–High Kamla Nagar Market (*p* = 0.002) and Tis Hazari Court (*p* = 0.028); Low–Low Madanpur Khadar and Dwarka Sector-12; outliers Civil Lines and Nizamuddin Railway Station; Ajmal Khan Road Market *p* = 0.066 (not treated as confirmed) |
| `pipeline_v2/advanced_analytics/7e_spatial_clustering_morans_i.csv` | 2 | Global Moran’s *I* for plastic burden (0.053) and PVC share |

**Method, as coded.** `pipeline_v2/07b_elite_spatial_stats.py` and `pipeline_v2/07c_local_hotspots.py`: *k* = 5 nearest neighbours, Haversine kilometres, inverse-distance weights, row-standardized, 999 conditional permutations. Exploratory site-wise *p*; no FDR across the 58 local tests.

### Object C: city plastic ledger (*N* = 2 records)

| File | What it holds | Values locked in the manuscript |
|---|---|---|
| `phase7c_city_system_metrics.csv` | Generation, processed, remainder | 1,117 TPD; 858 TPD; 259 TPD |
| `phase7c_city_performance_indicator.csv` | Processed/generated ratio | 76.81%; 85% is a study operating band, not a regulation |

**Primary source (third party, public filing).** Delhi Pollution Control Committee, *Monthly Progress Reports*, March 2025 and June 2025, Section VIII (Plastic Waste Management), submitted to the National Green Tribunal. Both months record the same two TPD figures. Bibliographic landing page used in `references.bib`: [https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi](https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi). These quantities are **not** taken from Annexure-5.

**Context only, different denominator.** Delhi Economic Survey 2025–26 mixed-MSW processed share ≈ 63% on ≈ 11,862 TPD generated (Planning Department, GNCTD; [https://delhiplanning.delhi.gov.in/](https://delhiplanning.delhi.gov.in/)). That mixed-MSW ledger is not added to the 259 TPD plastic remainder.

### Object D: WTE facility census (4 plants, March 2025)

| File | Rows | Locked values |
|---|---:|---|
| `phase7c_facility_utilization_classifications.csv` | 4 | Ghazipur 1,300 / 757.3 TPD = 58.3% (headroom to 85% = 347.7 TPD); Tehkhand 2,000 / 1,359.3 = 68.0% (340.7 TPD); Okhla 1,950 / 1,867.9 = 95.8% High Utilization; Bawana 2,000 / 2,167.5 = 108.4% Over-Stressed. Combined Ghazipur+Tehkhand mixed-waste headroom 688.4 TPD |

**Primary source.** DPCC March 2025 MPR, Annexure-5 (facility mixed-waste census snapshot, not a plastic-only capacity file). Headroom is mixed-waste throughput to the study’s 85% band. The 259 TPD plastic remainder and the 688.4 TPD mixed-waste headroom stay on separate ledgers.

**External operating context (not in the census file).** Ghazipur FY2025–26 shutdown days and CPCB affidavit compliance flags are cited from contemporaneous reporting and are **not** treated as measured emissions from these files.

### Object E: robustness gate (72 specification rows)

| File | Rows | What it is |
|---|---:|---|
| `phase7d_scenario_registry.csv` | 72 | Weighting, normalization, leave-one-out, missing-data and facility-benchmark rows |
| `phase7d_robust_priorities.csv` | 58 | Top-10 appearance among 9 weighting/normalization tests; GREEN names: Ridge, Kashmere Gate ISBT, CBD Karkardooma (each 8/9); DAV School 9/9 appearance but LOO-influential |
| `phase7d_leave_one_out_influence.csv` | 58 | Mean and maximum rank displacement of remaining names when a locality is removed |
| `phase7d_convergence_summary.csv` | -- | Mean Spearman *ρ* = 0.893; mean top-10 overlap 83.3%; mean LOO displacement 0.55 |

GREEN/AMBER/RED apply only to locality-priority classes. They are not reused for plants, ledgers or clusters.

### Object F: reverse-logistics constraint set

| File | What it is |
|---|---|
| `pipeline_v2/advanced_analytics/7h_bawana_diversion_routing.csv` | Scenario origins, candidate sinks (Ghazipur, Tehkhand), blocked node (Bawana), assumed extra km |
| `tables_csv/14_reverse_logistics.csv` | Manuscript Table 14 wording |

This is a constraint file, not a solved vehicle-routing timetable. Road network, fleet, time windows and costs are not in the repository because they were not observed.

### Manuscript tables (CSV)

`tables_csv/` holds Tables 1–16 and the Figure 8 decision screen, with manuscript wording. Index: `tables_csv/_index.csv`.

---

## Access conditions (explicit)

| Item | Condition |
|---|---|
| Repository | Public: [https://github.com/jainyogya07/Nature-Sustain](https://github.com/jainyogya07/Nature-Sustain) |
| Code licence | MIT (see `LICENSE`) |
| Compiled extracts | May be reused with citation of this repository and of the originating government report |
| Full SRI / DPCC / Economic Survey PDFs | Not redistributed here; download from the agency URLs above |
| Registration / fee / embargo | None |
| Human-subjects / ethics restriction | None; locality names are public place-names from a published government survey |
| Controlled access | None |
| Corresponding author for requests | Sonal Khurana, [sonal.khurana@gmail.com](mailto:sonal.khurana@gmail.com); response intended within 10 working days |

---

## Suggested data citations (Nature Portfolio / DataCite form)

Use after a Zenodo DOI exists. Until then, cite the GitHub repository in the Code/Data availability statements and cite the government reports as ordinary references.

1. Shriram Institute for Industrial Research. *Assessment and Characterization of Plastic Waste in NCT of Delhi*. Department of Environment, Government of NCT of Delhi [https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf](https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf) (2020).
2. Delhi Pollution Control Committee. *Monthly Progress Reports* (March and June 2025). [https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi](https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi) (2025).
3. Planning Department, Government of NCT of Delhi. *Delhi Economic Survey 2025–26*. [https://delhiplanning.delhi.gov.in/](https://delhiplanning.delhi.gov.in/) (2026).
4. Khurana, S. & Jain, Y. Evidence-linked decision architecture for circular plastic waste management in cities: data and code. GitHub [https://github.com/jainyogya07/Nature-Sustain](https://github.com/jainyogya07/Nature-Sustain) (2026). Replace this URL with the Zenodo DOI when minted.

---

## Policy mapping (so editors can see the statements are not generic)

| Nature Portfolio requirement | How this paper meets it |
|---|---|
| Minimum dataset for interpret / verify / extend | Objects A–F and `tables_csv/` in the GitHub repository |
| Primary vs referenced datasets named separately | Author compilations vs SRI 2020, DPCC MPR, Economic Survey, CPCB portals |
| Accession / persistent link | GitHub URL now; Zenodo DOI on acceptance (stated as pending, not fabricated) |
| Third-party administrative data | Agency named; public URLs given; full PDFs not copied; extracts deposited |
| Restrictions described precisely | MIT; no embargo; government copyright on source PDFs; contact email and 10-day response |
| Code as a separate section after Data availability | Done |
| Licence, restrictions, replication access | MIT; unrestricted; `requirements.txt` and script paths given |
| Figure source data | `figures/` plus the CSVs that feed each panel |
| Data citation in the reference list | Suggested DataCite lines above; DOI line to be updated after Zenodo |
