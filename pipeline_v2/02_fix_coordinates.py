#!/usr/bin/env python3
"""
=============================================================================
MODULE 2: COORDINATE REPAIR
Delhi-NCR Circular Plastic Assessment — Fix All Coordinate Issues
=============================================================================
Fixes:
  1. Madhipur: DMS '77°0.5'58.7"E' mis-parsed as 0.099639 → corrected to 77.099639
  2. Miranda House & JJ Colony: corrupt lat/lon → geocoded via OSM Nominatim
  3. All DMS coordinates → decimal degrees (uniform format)
  4. Each fix gets a confidence score and provenance note

Geocoding: OSM Nominatim (free, no API key needed).
Geocoded coordinates are flagged as 'geocoded' not 'field_survey'.
=============================================================================
"""

import csv
import re
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "pipeline_v2" / "audit"
OUT.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# DMS PARSER (from parse_coords.py — improved)
# ─────────────────────────────────────────────────────────────────────────────
def parse_dms(s):
    """Parse DMS string → decimal degrees. Returns (decimal, confidence, note)"""
    if not s or not str(s).strip():
        return None, 0.0, "empty"

    s = str(s).strip()

    # Already decimal
    try:
        val = float(s)
        if 20 < val < 35:   # plausible Delhi latitude
            return val, 1.0, "already_decimal_lat"
        if 74 < val < 80:   # plausible Delhi longitude
            return val, 1.0, "already_decimal_lon"
        if val < 10:
            return None, 0.0, f"decimal_out_of_range:{val}"
    except ValueError:
        pass

    # DMS with °'"
    pattern = r"(\d+)[°\s]+(\d+(?:\.\d+)?)['\s]+(\d+(?:\.\d+)?)[\"″\s]*([NSEW]?)"
    m = re.search(pattern, s)
    if m:
        d, mn, sec, direc = m.groups()
        dec = float(d) + float(mn) / 60 + float(sec) / 3600
        if direc in ("S", "W"):
            dec = -dec
        return round(dec, 6), 1.0, "dms_parsed"

    # DMS without seconds: 28°40'N
    pattern2 = r"(\d+)[°\s]+(\d+(?:\.\d+)?)['\s]*([NSEW]?)"
    m2 = re.search(pattern2, s)
    if m2:
        d, mn, direc = m2.groups()
        dec = float(d) + float(mn) / 60
        if direc in ("S", "W"):
            dec = -dec
        return round(dec, 6), 0.95, "dms_no_seconds"

    return None, 0.0, f"unparseable:{s[:40]}"


def fix_madhipur_longitude():
    """
    Source PDF text: '77°0.5'58.7"E'
    This DMS string was mis-read as just '0.099639' (the fractional minutes).
    Correct parse: 77° 0.5' 58.7" = 77 + 0.5/60 + 58.7/3600 = 77.024... 
    But actual DMS in PDF: 77°05'58.7"E → 77 + 5/60 + 58.7/3600 = 77.099639°
    The raw CSV shows the source DMS was '77°0.5'58.7"E' which renders as ~77.099°
    """
    # Re-parsing '77°0.5'58.7"E':
    # degrees=77, minutes=0.5+58.7/60? — that's ambiguous formatting
    # The decimal 0.099639 = (0*60 + 5*60 + 58.7)/(3600) ... actually:
    # 0.099639 ≈ 5'58.7" / 60 → so full longitude = 77° + 0.099639° = 77.099639
    # This confirms: Madhipur longitude = 77.099639°E (the '77°' was truncated by the extractor)
    corrected = 77.099639
    return corrected, 1.0, "corrected_from_dms_77deg0.5min58.7sec_E"


# ─────────────────────────────────────────────────────────────────────────────
# OSM NOMINATIM GEOCODER
# ─────────────────────────────────────────────────────────────────────────────
def geocode_nominatim(location_name, delhi_context=True):
    """
    Query OSM Nominatim for a location in Delhi.
    Returns (lat, lon, confidence, display_name) or (None, None, 0, error_msg).
    Rate limit: 1 request/second required by Nominatim ToS.
    """
    if delhi_context:
        query = f"{location_name}, Delhi, India"
    else:
        query = location_name

    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "limit": 1,
        "countrycodes": "in",
        "bounded": 1,
        "viewbox": "76.8,29.0,77.4,28.4"  # Delhi bounding box
    })

    url = f"https://nominatim.openstreetmap.org/search?{params}"
    headers = {
        "User-Agent": "DelhiPlasticResearch/1.0 (academic-research)"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        if data:
            result = data[0]
            lat = float(result["lat"])
            lon = float(result["lon"])
            display = result.get("display_name", "")

            # Confidence: check if result is within Delhi bounds
            if 28.4 <= lat <= 29.0 and 76.8 <= lon <= 77.4:
                conf = 0.75  # OSM match within Delhi bounds
            else:
                conf = 0.3   # Out of expected range
                print(f"    WARNING: OSM result outside Delhi bounds: {lat},{lon}")

            return lat, lon, conf, display
        else:
            return None, None, 0.0, "no_results"

    except Exception as e:
        return None, None, 0.0, f"error:{str(e)[:60]}"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN: PROCESS ALL COORDINATES
# ─────────────────────────────────────────────────────────────────────────────
def repair_all_coordinates():
    LOCALITY_CSV = BASE / "phase5c/data/locality_plastic_analysis.csv"

    with open(LOCALITY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    results = []

    print("\nProcessing coordinates for all 58 localities...")
    print("-" * 70)

    for i, row in enumerate(rows):
        loc = row.get("location", f"row_{i+2}").strip()
        lat_raw = row.get("latitude", "").strip()
        lon_raw = row.get("longitude", "").strip()

        coord_status = "field_survey"
        lat_dec = None
        lon_dec = None
        lat_conf = 0.0
        lon_conf = 0.0
        coord_note = ""

        # ---- SPECIAL CASE: Miranda House & JJ Colony (corrupt source data) ----
        corrupt_locs = {
            "Miranda House & Khalsa College": "Miranda House, Delhi University",
            "JJ Colony, Rajendra Park, Nangloi": "JJ Colony Rajendra Park Nangloi, Delhi"
        }

        if loc in corrupt_locs:
            print(f"  [{i+2}] {loc}: Source coordinates corrupted → geocoding via OSM...")
            search_name = corrupt_locs[loc]
            lat_dec, lon_dec, conf, display = geocode_nominatim(search_name)
            time.sleep(1.1)  # Nominatim rate limit: 1 req/sec

            if lat_dec:
                coord_status = "geocoded_osm"
                lat_conf = lon_conf = conf
                coord_note = f"OSM_geocoded | display: {display[:80]}"
                print(f"    → ({lat_dec:.6f}, {lon_dec:.6f}) conf={conf:.2f}")
            else:
                coord_status = "coordinate_error"
                coord_note = f"OSM_geocoding_failed: {display}"
                print(f"    → FAILED: {display}")

        # ---- SPECIAL CASE: Madhipur (truncated longitude) ----
        elif loc == "Madhipur":
            print(f"  [{i+2}] {loc}: Longitude truncated (0.099 → 77.099) → correcting...")
            lat_dec, lat_conf, lat_note = parse_dms(lat_raw)
            lon_dec, lon_conf, lon_note = fix_madhipur_longitude()
            coord_status = "corrected"
            coord_note = f"lon_corrected: DMS '77°0.5'58.7\"E' was truncated to 0.099639; full value = 77.099639"
            print(f"    → lat={lat_dec:.6f}, lon={lon_dec:.6f} (corrected)")

        # ---- NORMAL CASE: Parse DMS ----
        else:
            lat_dec, lat_conf, lat_note = parse_dms(lat_raw)
            lon_dec, lon_conf, lon_note = parse_dms(lon_raw)

            if lat_dec is None or lon_dec is None:
                coord_status = "coordinate_error"
                coord_note = f"lat_note={lat_note} lon_note={lon_note}"
                print(f"  [{i+2}] {loc}: Parse failed — lat_note={lat_note[:30]}, lon_note={lon_note[:30]}")
            else:
                # Delhi bounds check
                if not (28.3 <= lat_dec <= 29.1 and 76.8 <= lon_dec <= 77.5):
                    coord_status = "coordinate_warning"
                    coord_note = f"Out of Delhi bounds: ({lat_dec:.4f}, {lon_dec:.4f})"
                    print(f"  [{i+2}] {loc}: WARNING — coordinate out of Delhi bounds: {lat_dec:.4f}, {lon_dec:.4f}")
                else:
                    coord_status = "field_survey"
                    coord_note = f"dms_parsed: {lat_note}"

        results.append({
            "location": loc,
            "lat_raw": lat_raw,
            "lon_raw": lon_raw,
            "lat_decimal": round(lat_dec, 6) if lat_dec else None,
            "lon_decimal": round(lon_dec, 6) if lon_dec else None,
            "coordinate_status": coord_status,
            "coordinate_confidence": round(min(lat_conf, lon_conf), 2),
            "coordinate_note": coord_note
        })

    # ---- WRITE COORDINATE REGISTRY ----
    out_csv = OUT / "coordinate_registry.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # Summary
    statuses = {}
    for r in results:
        s = r["coordinate_status"]
        statuses[s] = statuses.get(s, 0) + 1

    print("\n" + "=" * 70)
    print("COORDINATE REPAIR SUMMARY")
    print("=" * 70)
    for s, c in sorted(statuses.items()):
        print(f"  {s:30s}: {c}")
    print(f"\n  Output: {out_csv}")
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("MODULE 2: COORDINATE REPAIR")
    print("=" * 70)
    results = repair_all_coordinates()
