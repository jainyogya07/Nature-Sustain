# Evidence-linked decision architecture for circular plastic waste management in cities

Replication repository for a *Nature Sustainability* manuscript.

**Authors.** Sonal Khurana (corresponding: [sonal.khurana@gmail.com](mailto:sonal.khurana@gmail.com)) and Yogay Jain, Vivekananda Institute of Professional Studies – Technical Campus, New Delhi.

**Canonical URL.** [https://github.com/jainyogya07/Nature-Sustain](https://github.com/jainyogya07/Nature-Sustain)

**Licence.** MIT (`LICENSE`).

Paste-ready **Data availability** and **Code availability** statements, with file-level verification, are in [`DATA_CODE_AVAILABILITY.md`](DATA_CODE_AVAILABILITY.md). That file follows Nature Portfolio policy: two separate sections, Data availability first, then Code availability.

## What this paper does

Urban circularity work often treats a locality resin share as recovery, a city processing ratio as plant capacity, or a high local burden as a hotspot. This repository keeps six evidence objects on separate ledgers and licenses intervention only at the scale of the supporting file:

| Object | Decision unit | Locked empirical result in this deposit |
|---|---|---|
| A. Locality composition | 58 complete-resin NCT localities | Plastic % from 1.98 (Okhla Mandi) to 30.49 (Kamla Nehru Ridge); Ridge = burden 1.000; Kashmere Gate ISBT 30.25% / 0.992; CBD Karkardooma 22.68% / 0.744 |
| B. Spatial association | Same 58 points | High–high: Kamla Nagar Market, Tis Hazari Court. Ridge and Kashmere Gate are not classified |
| C. City plastic ledger | Delhi NCT, two DPCC records | 858 of 1,117 TPD processed (76.81%); remainder 259 TPD; *N* = 2; no interval |
| D. WTE census | Four plants, March 2025 | 58.3–108.4%; Ghazipur/Tehkhand mixed-waste headroom to 85% = 688.4 TPD; Okhla 95.8% High Utilization; Bawana 108.4% over-stressed |
| E. Robustness gate | 72 specification rows | Mean Spearman ρ = 0.893; top-10 overlap 83.3%; only three of 58 names are GREEN |
| F. Constraint set | Scenario origins and sinks | Not a solved route. Bawana blocked; Okhla not treated as slack |

The architecture can be reused in another city. These ranks and tonnages cannot.

## Repository layout

```
DATA_CODE_AVAILABILITY.md   Nature Sustainability statements + verified inventory
Nature_Sustainability_Manuscript.md
Supplementary_Information.md
main.tex  references.bib     LaTeX source (APA / earlier compile path)
DATA_DICTIONARY.md
tables_csv/                 Tables 1–16 and Figure 8 as CSV
pipeline_v2/                Analysis scripts and the N=58 master CSV
  locality_plastic_analysis_v2.csv
  advanced_analytics/       LISA, diversion, inequality extracts
phase7c_*.csv               City ledger, resin summaries, WTE classes
phase7d_*.csv               72-row registry, appearance, LOO
figures/build_figures.py    Manuscript figures
sri_plastic_study_complete_extraction.csv
```

## Data (minimum set)

**Compiled locality file (use this first).** `pipeline_v2/locality_plastic_analysis_v2.csv` — 58 rows, 51 columns, including SRI table and page numbers, coordinates, sample mass, plastic %, and six-resin shares. This is an author compilation, not a new field survey.

**Underlying government report (public PDF, verified).** Shriram Institute for Industrial Research, *Assessment and Characterization of Plastic Waste in NCT of Delhi* (July 2020), Department of Environment, GNCTD: [https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf](https://environment.delhi.gov.in/sites/default/files/environment/universal/sri_plastic_study_1.pdf) (HTTP 200 on 18 November 2026; 4,090,547 bytes).

**City plastic ledger and plant census.** Extracted from DPCC Monthly Progress Reports to the National Green Tribunal (March and June 2025, Section VIII; March 2025 Annexure-5). Landing page cited in the bibliography: [https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi](https://www.dpcc.delhigovt.nic.in/monthlyprogressreportsofdelhi). Values in `phase7c_city_system_metrics.csv` and `phase7c_facility_utilization_classifications.csv`.

**Do not mix ledgers.** 259 TPD is plastic remainder. 688.4 TPD is mixed-waste headroom at two plants. The Economic Survey ≈63% figure is total MSW, a different denominator ([https://delhiplanning.delhi.gov.in/](https://delhiplanning.delhi.gov.in/)).

Full object-by-object paths: [`DATA_CODE_AVAILABILITY.md`](DATA_CODE_AVAILABILITY.md).

## Code

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

| Task | Script |
|---|---|
| Local Moran’s I / Kruskal–Wallis | `pipeline_v2/07b_elite_spatial_stats.py` |
| Site-wise LISA labels | `pipeline_v2/07c_local_hotspots.py` |
| Manuscript figures | `figures/build_figures.py` |

Scripts resolve the project root from `__file__`. They do not require a machine-specific path.

Python ≥ 3.10. Spatial weights are implemented in-repo (Haversine *k* = 5, inverse-distance, row-standardized, 999 permutations); PySAL is not required.

## What is deliberately not in this repository

- Full third-party PDFs of SRI, DPCC, CPCB or Economic Survey reports (agency copyright; use the URLs above).
- A solved vehicle-routing timetable, GPS traces, fleet file, or cost matrix (not observed).
- Capture or recycling rates (not measured; PET/PP are prevalence).
- A Zenodo DOI (not minted at first deposit; will be added on the acceptance release).

## Cite

Until a journal version of record exists, cite the manuscript title, authors, and this repository. After Zenodo archival, replace the GitHub URL with the DOI in DataCite form as set out in `DATA_CODE_AVAILABILITY.md`.
