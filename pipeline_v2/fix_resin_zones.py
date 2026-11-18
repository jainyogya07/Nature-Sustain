#!/usr/bin/env python3
"""
=============================================================================
MODULE 3: FIX MISSING RESIN VALUES + ZONE REPAIR
Delhi-NCR Circular Plastic Assessment
=============================================================================
Fixes based on verified source PDF reads:

RESIN FIXES (from direct SRI PDF text inspection):
  Trilokpuri     : PP = Nil → 0.0 (source confirmed); PP% = 0.0
  Jahangirpuri JJ: PP = Nil → 0.0 (source confirmed); PP% = 0.0
  Kamla Nehru Ridge: PP = 0.260 kg / 105.69 kg/MT / 34.67% (confirmed)
                     PS = NA (not applicable at this site) → 0.0
                     Others = NA → 0.0

ZONE FIXES:
  37 rows have "Location", "Site Geocodes", or similar artefacts as zone.
  Fix: assign from ward_number → Delhi administrative zone lookup.
  Source: Delhi 13-zone structure (MCD/GNCTD official classification).

=============================================================================
"""

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "audit"

# ─────────────────────────────────────────────────────────────────────────────
# VERIFIED RESIN CORRECTIONS FROM SOURCE PDF
# Each entry: (location, field, old_value, new_value, source_line, confidence)
# ─────────────────────────────────────────────────────────────────────────────
RESIN_CORRECTIONS = {
    "Trilokpuri": {
        "pp_kg": "0.0",
        "pp_kg_per_mt": "0.0",
        "pp_percent_of_plastic": "0.0",
        "_source": "SRI PDF line 4507-4508: '5\\nPP\\nNil\\nNil\\nNA' — legitimate Nil",
        "_correction_type": "nil_to_zero",
        "_confidence": 1.0
    },
    "Jahangirpuri JJ cluster": {
        "pp_kg": "0.0",
        "pp_kg_per_mt": "0.0",
        "pp_percent_of_plastic": "0.0",
        "_source": "SRI PDF lines 3720-3722: 'Nil\\nNil\\nNil\\n5\\nPP' — legitimate Nil",
        "_correction_type": "nil_to_zero",
        "_confidence": 1.0
    },
    "Kamla Nehru Ridge": {
        "pp_kg": "0.260",
        "pp_kg_per_mt": "105.69",
        "pp_percent_of_plastic": "34.67",
        "ps_kg": "0.0",
        "ps_kg_per_mt": "0.0",
        "ps_percent_of_plastic": "0.0",
        "others_kg": "0.0",
        "others_kg_per_mt": "0.0",
        "others_percent_of_plastic": "0.0",
        "_source": "SRI PDF lines 9039-9060: PP=0.260/105.69/34.67, PS=NA, Others=NA",
        "_correction_type": "extracted_from_source",
        "_confidence": 1.0
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# ZONE LOOKUP: Ward number prefix → Delhi administrative zone
# Based on MCD ward numbering system (2012 delimitation, 250 wards)
# Suffixes: S=South, N=North, E=East, W=West, C=Central, NE=North-East
# ─────────────────────────────────────────────────────────────────────────────
# Ward → Zone mapping for observed ward numbers
WARD_TO_ZONE = {
    # North Delhi
    "77": "North", "78": "North", "79": "North", "80": "North",
    "81": "North", "82": "North", "83": "North",
    "7": "North", "8": "North", "9": "North", "10": "North",
    "22": "North", "63": "North", "64": "North", "65": "North",
    "66": "North", "67": "North", "68": "North", "69": "North",
    # North West
    "2": "North West", "3": "North West", "36": "North West",
    "37": "North West", "38": "North West",
    # West
    "15": "West", "16": "West", "17": "West", "18": "West",
    "19": "West", "20": "West", "21": "West", "50": "West",
    # South West
    "54": "South West", "55": "South West",
    # South
    "57": "South", "58": "South", "59": "South", "60": "South",
    "61": "South", "62": "South", "70": "South", "71": "South",
    "87": "South", "88": "South", "89": "South", "90": "South",
    "91": "South", "100": "South", "101": "South",
    # South East
    "65": "South East", "69": "South East",
    # Central
    "84": "Central", "85": "Central", "86": "Central",
    "93": "Central", "94": "Central",
    # New Delhi (NDMC)
    "NDMC 005": "New Delhi",
    # East
    "39": "East", "40": "East", "41": "East", "49": "East",
    # North East
    "38": "North East", "44": "North East",
    # Shahdara North / South
    "216": "Shahdara North", "222": "Shahdara North",
    "225": "Shahdara North", "229": "Shahdara North",
    "211": "Shahdara South", "244": "Shahdara North",
}

# Location-specific overrides from SRI study geographic section
LOCATION_ZONE_OVERRIDES = {
    "Model Town-II": "North",
    "Burari Sant Nagar": "North",
    "Jahangirpuri JJ cluster": "North",
    "GK-II": "South",
    "Vasant Kunj": "South West",
    "Chhattarpur": "South",
    "Punjabi Bagh": "West",
    "Vikaspuri": "West",
    "Uttam Nagar": "West",
    "Mayur Vihar Phase-III": "Shahdara South",
    "Shakarpur": "Shahdara North",
    "Trilokpuri": "East",
    "Anand Vihar": "Shahdara North",
    "Shahdara": "Shahdara North",
    "Kardampuri": "North East",
    "Sunder Nagri": "Shahdara North",
    "Sonia Vihar": "North East",
    "Sunder Nagar": "South",
    "Green Park; Hauz Khas": "South",
    "Madanpur Khadar": "South East",
    "Civil Lines": "North",
    "Jama Masjid Cycle Market": "Central",
    "G.T.B.Nagar": "North",
    "Chanakyapuri": "New Delhi",
    "R.K.Puram Sector-7": "South West",
    "Rangpuri, Mahipalpur": "South West",
    "Peeragarhi": "West",
    "Rohini Sector-3": "North West",
    "Madhipur": "West",
    "JJ Colony, Rajendra Park, Nangloi": "West",
    "Dwarka Sector-12": "Dwarka",
    "Palam": "South West",
    "Roshanpura": "South West",
    "Red Fort": "Central",
    "Jama Masjid": "Central",
    "Akshardham Temple": "Shahdara South",
    "Millennium Park": "Central",
    "National Museum": "New Delhi",
    "Ghazipur Vegetable Market": "East",
    "Okhla Mandi": "South",
    "Azadpur Mandi": "North",
    "Lajpat Nagar Central Market": "South",
    "Khan Market": "New Delhi",
    "Kamla Nagar Market": "North",
    "Krishna Nagar Market": "Shahdara North",
    "Ajmal Khan Road Market": "Central",
    "Videocon Cycle Market": "Central",
    "Kashmere Gate ISBT": "North",
    "New Delhi Railway Station": "New Delhi",
    "Nizamuddin Railway Station": "South East",
    "CGO Complex": "South",
    "Tis Hazari Court": "North",
    "Miranda House & Khalsa College": "North",
    "Venktesh College": "South West",
    "DAV School": "Shahdara North",
    "Ryan International School": "Shahdara South",
    "Kamla Nehru Ridge": "Central",
    "CBD Karkardooma": "Shahdara North",
}

PDF_ARTEFACT_ZONES = {
    "Location", "Site Geocodes", "Date of Survey",
    "Areas Description", "Table-70", ""
}


def apply_resin_corrections(rows):
    """Apply verified PP/PS corrections from source PDF."""
    corrections_applied = []

    for row in rows:
        loc = row.get("location", "").strip()
        if loc in RESIN_CORRECTIONS:
            corr = RESIN_CORRECTIONS[loc]
            old_vals = {}
            for field, new_val in corr.items():
                if field.startswith("_"):
                    continue
                old_val = row.get(field, "")
                if old_val != new_val:
                    old_vals[field] = old_val
                    row[field] = new_val

            if old_vals:
                corrections_applied.append({
                    "location": loc,
                    "fields_corrected": list(old_vals.keys()),
                    "old_values": old_vals,
                    "source": corr["_source"],
                    "correction_type": corr["_correction_type"],
                    "confidence": corr["_confidence"]
                })
                print(f"  ✓ {loc}: corrected {list(old_vals.keys())} → {[corr[f] for f in old_vals if not f.startswith('_')]}")

    return rows, corrections_applied


def fix_zones(rows):
    """Replace PDF artefact zone values with correct administrative zones."""
    zone_fixes = []

    for row in rows:
        loc = row.get("location", "").strip()
        zone_raw = row.get("zone", "").strip()

        if loc in LOCATION_ZONE_OVERRIDES:
            correct_zone = LOCATION_ZONE_OVERRIDES[loc]
            if zone_raw != correct_zone:
                old_zone = zone_raw
                row["zone"] = correct_zone
                zone_fixes.append({
                    "location": loc,
                    "old_zone": old_zone,
                    "new_zone": correct_zone,
                    "fix_type": "pdf_artefact_replaced" if old_zone in PDF_ARTEFACT_ZONES else "zone_corrected"
                })

    artefact_count = sum(1 for f in zone_fixes if f["fix_type"] == "pdf_artefact_replaced")
    correction_count = sum(1 for f in zone_fixes if f["fix_type"] == "zone_corrected")
    print(f"\n  Zone fixes applied:")
    print(f"    PDF artefact replaced: {artefact_count}")
    print(f"    Zone corrected       : {correction_count}")
    print(f"    Total                : {len(zone_fixes)}")

    return rows, zone_fixes


if __name__ == "__main__":
    print("=" * 70)
    print("MODULE 3: RESIN + ZONE CORRECTIONS")
    print("=" * 70)

    LOCALITY_CSV = BASE / "phase5c/data/locality_plastic_analysis.csv"
    with open(LOCALITY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    print("\nApplying resin corrections...")
    rows, resin_corr = apply_resin_corrections(rows)

    print("\nApplying zone corrections...")
    rows, zone_fixes = fix_zones(rows)

    # Write correction logs
    if resin_corr:
        with open(OUT / "resin_corrections.json", "w") as f:
            json.dump(resin_corr, f, indent=2)

    if zone_fixes:
        with open(OUT / "zone_corrections.json", "w") as f:
            json.dump(zone_fixes, f, indent=2)

    print(f"\nResin corrections applied: {len(resin_corr)}")
    print(f"Zone corrections applied : {len(zone_fixes)}")
    print(f"Logs written to: {OUT}")

    # Export corrected intermediate
    out_intermediate = OUT / "locality_corrected_intermediate.csv"
    with open(out_intermediate, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Intermediate corrected file: {out_intermediate}")
