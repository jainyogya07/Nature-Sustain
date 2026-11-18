#!/usr/bin/env python3
"""
=============================================================================
MODULE 4: REBUILD AUTHORITATIVE MASTER DATASET
Delhi-NCR Circular Plastic Assessment
=============================================================================
Rebuilds locality_plastic_analysis_v2.csv from scratch with:
  - All coordinate fixes from Module 2
  - All resin/zone fixes from Module 3
  - Per-row data quality flags
  - Full provenance metadata (PDF table number, page, survey date)
  - Explicit NULL vs zero distinction
  - N=58 restored (was N=55 due to fixable missing values)
  - Compositionality validation on every row
  - Income level standardised
  - Land use type standardised

Output: pipeline_v2/locality_plastic_analysis_v2.csv
=============================================================================
"""

import csv
import json
import re
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
AUDIT_OUT = BASE / "pipeline_v2" / "audit"
OUT = BASE / "pipeline_v2"
OUT.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# IMPORT HELPERS FROM OTHER MODULES
# ─────────────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(BASE / "pipeline_v2"))

# Inline DMS parser (avoids import dependency)
def parse_dms(s):
    if not s or not str(s).strip():
        return None
    s = str(s).strip()
    try:
        val = float(s)
        if 20 < val < 35 or 74 < val < 80:
            return round(val, 6)
        if val < 10:
            return None
    except ValueError:
        pass
    pattern = r"(\d+)[°\s]+(\d+(?:\.\d+)?)['\s]+(\d+(?:\.\d+)?)[\"″\s]*([NSEW]?)"
    m = re.search(pattern, s)
    if m:
        d, mn, sec, direc = m.groups()
        dec = float(d) + float(mn)/60 + float(sec)/3600
        if direc in ("S","W"): dec = -dec
        return round(dec, 6)
    pattern2 = r"(\d+)[°\s]+(\d+(?:\.\d+)?)['\s]*([NSEW]?)"
    m2 = re.search(pattern2, s)
    if m2:
        d, mn, direc = m2.groups()
        dec = float(d) + float(mn)/60
        if direc in ("S","W"): dec = -dec
        return round(dec, 6)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# CORRECTIONS — from Module 3
# ─────────────────────────────────────────────────────────────────────────────
from fix_resin_zones import RESIN_CORRECTIONS, LOCATION_ZONE_OVERRIDES, PDF_ARTEFACT_ZONES

# Coordinate corrections
COORD_CORRECTIONS = {
    "Madhipur": {
        "lat_decimal": 28.679167,    # 28°40'45.3"N correctly parsed
        "lon_decimal": 77.099639,    # 77°05'58.7"E — truncation corrected
        "coordinate_status": "corrected",
        "coordinate_note": "Longitude '77°0.5'58.7\"E' was truncated to 0.099639; corrected to 77.099639"
    }
}

# Geocoded (from Module 2 output, if available; else use defaults)
GEOCODED_COORDS = {}
coord_registry = AUDIT_OUT / "coordinate_registry.csv"
if coord_registry.exists():
    with open(coord_registry, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["coordinate_status"] in ("geocoded_osm", "corrected"):
                GEOCODED_COORDS[row["location"]] = {
                    "lat_decimal": float(row["lat_decimal"]) if row["lat_decimal"] else None,
                    "lon_decimal": float(row["lon_decimal"]) if row["lon_decimal"] else None,
                    "coordinate_status": row["coordinate_status"],
                    "coordinate_note": row["coordinate_note"]
                }

# SRI study provenance metadata (table numbers from PDF TOC)
SRI_PROVENANCE = {
    "Model Town-II":              {"sri_table": "Table-1",  "sri_page": 16, "survey_date": ""},
    "Burari Sant Nagar":          {"sri_table": "Table-2",  "sri_page": 17, "survey_date": ""},
    "Jahangirpuri JJ cluster":    {"sri_table": "Table-3",  "sri_page": 17, "survey_date": "26.08.2019"},
    "GK-II":                      {"sri_table": "Table-4",  "sri_page": 19, "survey_date": ""},
    "Vasant Kunj":                {"sri_table": "Table-5",  "sri_page": 19, "survey_date": ""},
    "Chhattarpur":                {"sri_table": "Table-6",  "sri_page": 20, "survey_date": ""},
    "Punjabi Bagh":               {"sri_table": "Table-7",  "sri_page": 22, "survey_date": ""},
    "Vikaspuri":                  {"sri_table": "Table-8",  "sri_page": 22, "survey_date": ""},
    "Uttam Nagar":                {"sri_table": "Table-9",  "sri_page": 23, "survey_date": ""},
    "Mayur Vihar Phase-III":      {"sri_table": "Table-10", "sri_page": 25, "survey_date": ""},
    "Shakarpur":                  {"sri_table": "Table-11", "sri_page": 25, "survey_date": ""},
    "Trilokpuri":                 {"sri_table": "Table-12", "sri_page": 26, "survey_date": "16.10.2019"},
    "Anand Vihar":                {"sri_table": "Table-13", "sri_page": 28, "survey_date": ""},
    "Shahdara":                   {"sri_table": "Table-14", "sri_page": 29, "survey_date": ""},
    "Kardampuri":                 {"sri_table": "Table-15", "sri_page": 29, "survey_date": ""},
    "Sunder Nagri":               {"sri_table": "Table-16", "sri_page": 30, "survey_date": ""},
    "Sonia Vihar":                {"sri_table": "Table-17", "sri_page": 31, "survey_date": ""},
    "Sunder Nagar":               {"sri_table": "Table-18", "sri_page": 33, "survey_date": ""},
    "Green Park; Hauz Khas":      {"sri_table": "Table-19", "sri_page": 33, "survey_date": "29.09.2019"},
    "Madanpur Khadar":            {"sri_table": "Table-20", "sri_page": 34, "survey_date": ""},
    "Civil Lines":                {"sri_table": "Table-21", "sri_page": 36, "survey_date": ""},
    "Jama Masjid Cycle Market":   {"sri_table": "Table-22", "sri_page": 37, "survey_date": "19.08.2019"},
    "G.T.B.Nagar":                {"sri_table": "Table-23", "sri_page": 37, "survey_date": ""},
    "Chanakyapuri":               {"sri_table": "Table-24", "sri_page": 38, "survey_date": ""},
    "R.K.Puram Sector-7":        {"sri_table": "Table-25", "sri_page": 39, "survey_date": ""},
    "Rangpuri, Mahipalpur":       {"sri_table": "Table-26", "sri_page": 40, "survey_date": ""},
    "Peeragarhi":                 {"sri_table": "Table-27", "sri_page": 41, "survey_date": ""},
    "Rohini Sector-3":            {"sri_table": "Table-28", "sri_page": 42, "survey_date": ""},
    "Madhipur":                   {"sri_table": "Table-29", "sri_page": 43, "survey_date": ""},
    "JJ Colony, Rajendra Park, Nangloi": {"sri_table": "Table-30", "sri_page": 44, "survey_date": ""},
    "Dwarka Sector-12":           {"sri_table": "Table-31", "sri_page": 45, "survey_date": ""},
    "Palam":                      {"sri_table": "Table-32", "sri_page": 46, "survey_date": ""},
    "Roshanpura":                 {"sri_table": "Table-33", "sri_page": 47, "survey_date": ""},
    "Red Fort":                   {"sri_table": "Table-34", "sri_page": 48, "survey_date": ""},
    "Jama Masjid":                {"sri_table": "Table-35", "sri_page": 49, "survey_date": ""},
    "Akshardham Temple":          {"sri_table": "Table-36", "sri_page": 50, "survey_date": ""},
    "Millennium Park":            {"sri_table": "Table-37", "sri_page": 51, "survey_date": ""},
    "National Museum":            {"sri_table": "Table-38", "sri_page": 52, "survey_date": ""},
    "Ghazipur Vegetable Market":  {"sri_table": "Table-39", "sri_page": 53, "survey_date": "30.09.2019"},
    "Okhla Mandi":                {"sri_table": "Table-40", "sri_page": 54, "survey_date": ""},
    "Azadpur Mandi":              {"sri_table": "Table-41", "sri_page": 55, "survey_date": ""},
    "Lajpat Nagar Central Market":{"sri_table": "Table-42", "sri_page": 56, "survey_date": "20.11.2019"},
    "Khan Market":                {"sri_table": "Table-43", "sri_page": 57, "survey_date": ""},
    "Kamla Nagar Market":         {"sri_table": "Table-44", "sri_page": 58, "survey_date": ""},
    "Krishna Nagar Market":       {"sri_table": "Table-45", "sri_page": 59, "survey_date": ""},
    "Ajmal Khan Road Market":     {"sri_table": "Table-46", "sri_page": 60, "survey_date": "14.02.2020"},
    "Videocon Cycle Market":      {"sri_table": "Table-47", "sri_page": 61, "survey_date": "15.02.2020"},
    "Kashmere Gate ISBT":         {"sri_table": "Table-48", "sri_page": 62, "survey_date": ""},
    "New Delhi Railway Station":  {"sri_table": "Table-49", "sri_page": 63, "survey_date": "03.12.2019"},
    "Nizamuddin Railway Station": {"sri_table": "Table-50", "sri_page": 64, "survey_date": "18.12.2019"},
    "CGO Complex":                {"sri_table": "Table-51", "sri_page": 65, "survey_date": ""},
    "Tis Hazari Court":           {"sri_table": "Table-52", "sri_page": 66, "survey_date": ""},
    "Miranda House & Khalsa College": {"sri_table": "Table-53", "sri_page": 67, "survey_date": ""},
    "Venktesh College":           {"sri_table": "Table-54", "sri_page": 68, "survey_date": ""},
    "DAV School":                 {"sri_table": "Table-55", "sri_page": 69, "survey_date": ""},
    "Ryan International School":  {"sri_table": "Table-56", "sri_page": 70, "survey_date": "15.02.2020"},
    "Kamla Nehru Ridge":          {"sri_table": "Table-71", "sri_page": 76, "survey_date": "20.12.2019"},
    "CBD Karkardooma":            {"sri_table": "Table-72", "sri_page": 77, "survey_date": "11.02.2020"},
}

# Income level standardization
INCOME_STANDARD = {
    "High & Medium Income": "High-Middle",
    "High & Middle Income": "High-Middle",
    "Middle & High Income": "High-Middle",
    "Middle Income": "Middle",
    "High Income": "High",
    "Low Income": "Low",
    "Slum": "Slum",
    "Slum & Low Income": "Slum",
    "Other": "Other",
    "Middle": "Middle",
    "High": "High",
    "Low": "Low",
}

# Land use standardization
LAND_USE_STANDARD = {
    "Residential": "Residential",
    "Commercial": "Commercial",
    "Market": "Commercial",
    "Institutional": "Institutional",
    "Educational": "Institutional",
    "Office Complex": "Institutional",
    "Tourist": "Tourist",
    "Tourist Area": "Tourist",
    "Tourism": "Tourist",
    "Public Places": "Public",
    "Public": "Public",
    "Institutional Area": "Institutional",
    "Mixed": "Mixed",
    "Miscellaneous LU": "Mixed",
    "Miscellaneous": "Mixed",
    "Market Area": "Commercial",
}


def safe_float(v, default=None):
    if v is None or str(v).strip() in ("", "NA", "N/A", "na"):
        return default
    try:
        return float(str(v).strip())
    except (ValueError, TypeError):
        return default


def build_quality_flags(row_out):
    """Return a pipe-separated string of quality flags for this row."""
    flags = []

    # Coordinate status
    cstatus = row_out.get("coordinate_status", "")
    if cstatus == "geocoded_osm":
        flags.append("COORD_GEOCODED")
    elif cstatus == "corrected":
        flags.append("COORD_CORRECTED")
    elif cstatus == "coordinate_error":
        flags.append("COORD_MISSING")
    elif cstatus == "coordinate_warning":
        flags.append("COORD_OOB")

    # Resin corrections
    if row_out.get("resin_corrected"):
        flags.append("RESIN_CORRECTED")

    # Zone corrections
    if row_out.get("zone_corrected"):
        flags.append("ZONE_CORRECTED")

    # Small sample
    sample_kg = safe_float(row_out.get("waste_sample_kg"))
    if sample_kg is not None and sample_kg < 10:
        flags.append("SMALL_SAMPLE_LT10KG")

    # Compositionality
    resin_cols = [
        "pet_percent_of_plastic", "hdpe_ldpe_percent_of_plastic",
        "pvc_percent_of_plastic", "pp_percent_of_plastic",
        "ps_percent_of_plastic", "others_percent_of_plastic"
    ]
    vals = [safe_float(row_out.get(c)) for c in resin_cols]
    vals = [v for v in vals if v is not None]
    if vals:
        total = sum(vals)
        if total > 101:
            flags.append(f"RESIN_SUM_EXCEEDS_100:{total:.1f}")
        elif total < 85:
            flags.append(f"RESIN_SUM_LOW:{total:.1f}")

    return "|".join(flags) if flags else "OK"


def rebuild_master():
    LOCALITY_CSV = BASE / "phase5c/data/locality_plastic_analysis.csv"

    with open(LOCALITY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # New fieldnames for v2
    v2_fields = [
        # Provenance
        "source_document", "source_organization", "publication_year",
        "sri_table_number", "sri_page_number",
        # Location
        "location", "zone", "ward_numbers", "area_category",
        "income_level", "land_use_type",
        # Dates
        "survey_date",
        # Coordinates
        "latitude_dms", "longitude_dms",
        "latitude_decimal", "longitude_decimal",
        "coordinate_status", "coordinate_confidence", "coordinate_note",
        # Sample
        "waste_sample_kg", "plastic_sorted_kg",
        "plastic_kg_per_mt", "plastic_percent",
        # Resin composition (kg)
        "pet_kg", "hdpe_ldpe_kg", "pvc_kg", "pp_kg", "ps_kg", "others_kg",
        # Resin composition (kg/MT)
        "pet_kg_per_mt", "hdpe_ldpe_kg_per_mt", "pvc_kg_per_mt",
        "pp_kg_per_mt", "ps_kg_per_mt", "others_kg_per_mt",
        # Resin composition (%)
        "pet_percent_of_plastic", "hdpe_ldpe_percent_of_plastic",
        "pvc_percent_of_plastic", "pp_percent_of_plastic",
        "ps_percent_of_plastic", "others_percent_of_plastic",
        # Derived
        "resin_sum_check",
        # Analytical sample flags
        "in_n55_original",  # Was in original N=55 (complete resin)
        "in_n58_v2",        # In v2 N=58 (after PP/PS fixes)
        # Quality metadata
        "data_quality_flags", "resin_corrected", "zone_corrected",
        # Provenance chain
        "provenance_code", "geography_level",
        "pipeline_version", "row_created_at"
    ]

    output_rows = []
    n55_orig = 0
    n58_v2 = 0

    RESIN_COLS_PCT = [
        "pet_percent_of_plastic", "hdpe_ldpe_percent_of_plastic",
        "pvc_percent_of_plastic", "pp_percent_of_plastic",
        "ps_percent_of_plastic", "others_percent_of_plastic"
    ]

    for i, row in enumerate(rows, start=2):
        loc = row.get("location", "").strip()
        if not loc:
            continue

        # ── Apply resin corrections ──
        resin_corrected = False
        if loc in RESIN_CORRECTIONS:
            corr = RESIN_CORRECTIONS[loc]
            for field, val in corr.items():
                if not field.startswith("_"):
                    row[field] = val
            resin_corrected = True

        # ── Get correct zone ──
        zone_corrected = False
        orig_zone = row.get("zone", "").strip()
        correct_zone = LOCATION_ZONE_OVERRIDES.get(loc, orig_zone)
        if correct_zone != orig_zone:
            zone_corrected = True

        # ── Get coordinates ──
        lat_dms = row.get("latitude", "").strip()
        lon_dms = row.get("longitude", "").strip()

        if loc in GEOCODED_COORDS:
            gc = GEOCODED_COORDS[loc]
            lat_dec = gc.get("lat_decimal")
            lon_dec = gc.get("lon_decimal")
            coord_status = gc.get("coordinate_status", "geocoded_osm")
            coord_conf = 0.75
            coord_note = gc.get("coordinate_note", "")
        elif loc in COORD_CORRECTIONS:
            cc = COORD_CORRECTIONS[loc]
            lat_dec = cc["lat_decimal"]
            lon_dec = cc["lon_decimal"]
            coord_status = cc["coordinate_status"]
            coord_conf = 0.95
            coord_note = cc["coordinate_note"]
        else:
            lat_dec = parse_dms(lat_dms)
            lon_dec = parse_dms(lon_dms)
            if lat_dec is None or lon_dec is None:
                coord_status = "coordinate_error"
                coord_conf = 0.0
                coord_note = "Parse failed — check source PDF"
            elif not (28.3 <= lat_dec <= 29.1 and 76.8 <= lon_dec <= 77.5):
                coord_status = "coordinate_warning"
                coord_conf = 0.5
                coord_note = f"Out of Delhi bounds: ({lat_dec:.4f}, {lon_dec:.4f})"
            else:
                coord_status = "field_survey"
                coord_conf = 1.0
                coord_note = "DMS parsed from SRI field survey"

        # ── Income standardization ──
        income_raw = row.get("income_level", row.get("area_category", "")).strip()
        income_std = INCOME_STANDARD.get(income_raw, income_raw)

        # ── Land use standardization ──
        lu_raw = row.get("land_use_type", "").strip()
        lu_std = LAND_USE_STANDARD.get(lu_raw, lu_raw)

        # ── Resin sum ──
        resin_vals = [safe_float(row.get(c)) for c in RESIN_COLS_PCT]
        resin_vals_present = [v for v in resin_vals if v is not None]
        resin_sum = round(sum(resin_vals_present), 2) if resin_vals_present else None

        # ── N=55 / N=58 classification ──
        all_resin_present = all(safe_float(row.get(c)) is not None for c in RESIN_COLS_PCT)
        was_in_n55 = all(row.get(c, "").strip() not in ("", "NA") for c in RESIN_COLS_PCT)
        is_in_n58_v2 = all_resin_present

        if was_in_n55:
            n55_orig += 1
        if is_in_n58_v2:
            n58_v2 += 1

        # ── Provenance ──
        prov = SRI_PROVENANCE.get(loc, {})

        # ── Build output row ──
        row_out = {
            "source_document": "Assessment and Characterization of Plastic Waste in NCT of Delhi (July 2020)",
            "source_organization": "Shriram Institute for Industrial Research (SRI), commissioned by Dept of Environment, GNCTD",
            "publication_year": 2020,
            "sri_table_number": prov.get("sri_table", ""),
            "sri_page_number": prov.get("sri_page", ""),
            "location": loc,
            "zone": correct_zone,
            "ward_numbers": row.get("ward_numbers", "").strip(),
            "area_category": row.get("area_category", "").strip(),
            "income_level": income_std,
            "land_use_type": lu_std,
            "survey_date": row.get("survey_date", prov.get("survey_date", "")).strip(),
            "latitude_dms": lat_dms,
            "longitude_dms": lon_dms,
            "latitude_decimal": lat_dec,
            "longitude_decimal": lon_dec,
            "coordinate_status": coord_status,
            "coordinate_confidence": coord_conf,
            "coordinate_note": coord_note,
            "waste_sample_kg": row.get("waste_sample_kg", "").strip(),
            "plastic_sorted_kg": row.get("plastic_sorted_kg", "").strip(),
            "plastic_kg_per_mt": row.get("plastic_kg_per_mt", "").strip(),
            "plastic_percent": row.get("plastic_percent", "").strip(),
            "pet_kg": row.get("pet_kg", "").strip(),
            "hdpe_ldpe_kg": row.get("hdpe_ldpe_kg", "").strip(),
            "pvc_kg": row.get("pvc_kg", "").strip(),
            "pp_kg": row.get("pp_kg", "").strip(),
            "ps_kg": row.get("ps_kg", "").strip(),
            "others_kg": row.get("others_kg", "").strip(),
            "pet_kg_per_mt": row.get("pet_kg_per_mt", "").strip(),
            "hdpe_ldpe_kg_per_mt": row.get("hdpe_ldpe_kg_per_mt", "").strip(),
            "pvc_kg_per_mt": row.get("pvc_kg_per_mt", "").strip(),
            "pp_kg_per_mt": row.get("pp_kg_per_mt", "").strip(),
            "ps_kg_per_mt": row.get("ps_kg_per_mt", "").strip(),
            "others_kg_per_mt": row.get("others_kg_per_mt", "").strip(),
            "pet_percent_of_plastic": safe_float(row.get("pet_percent_of_plastic")),
            "hdpe_ldpe_percent_of_plastic": safe_float(row.get("hdpe_ldpe_percent_of_plastic")),
            "pvc_percent_of_plastic": safe_float(row.get("pvc_percent_of_plastic")),
            "pp_percent_of_plastic": safe_float(row.get("pp_percent_of_plastic")),
            "ps_percent_of_plastic": safe_float(row.get("ps_percent_of_plastic")),
            "others_percent_of_plastic": safe_float(row.get("others_percent_of_plastic")),
            "resin_sum_check": resin_sum,
            "in_n55_original": was_in_n55,
            "in_n58_v2": is_in_n58_v2,
            "resin_corrected": resin_corrected,
            "zone_corrected": zone_corrected,
            "provenance_code": "A",
            "geography_level": "Ward/Locality",
            "pipeline_version": "v2.0",
            "row_created_at": datetime.now().isoformat()
        }

        # Add quality flags after building row
        row_out["data_quality_flags"] = build_quality_flags(row_out)

        output_rows.append(row_out)

    # ── WRITE OUTPUT ──
    out_csv = OUT / "locality_plastic_analysis_v2.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=v2_fields)
        writer.writeheader()
        writer.writerows(output_rows)

    print("=" * 70)
    print("MODULE 4: MASTER REBUILD COMPLETE")
    print("=" * 70)
    print(f"  Total rows          : {len(output_rows)}")
    print(f"  Original N=55       : {n55_orig}")
    print(f"  Restored N=58 v2    : {n58_v2}")
    print(f"  Gain                : +{n58_v2 - n55_orig} rows restored")
    print(f"  Resin corrected     : {sum(1 for r in output_rows if r['resin_corrected'])}")
    print(f"  Zone corrected      : {sum(1 for r in output_rows if r['zone_corrected'])}")
    print(f"  Coords: field_survey: {sum(1 for r in output_rows if r['coordinate_status']=='field_survey')}")
    print(f"  Coords: corrected   : {sum(1 for r in output_rows if r['coordinate_status']=='corrected')}")
    print(f"  Coords: geocoded_osm: {sum(1 for r in output_rows if r['coordinate_status']=='geocoded_osm')}")
    print(f"  Coords: errors      : {sum(1 for r in output_rows if r['coordinate_status']=='coordinate_error')}")
    print(f"\n  Output: {out_csv}")

    return output_rows, n58_v2


if __name__ == "__main__":
    rows, n = rebuild_master()
