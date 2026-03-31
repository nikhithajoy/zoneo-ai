"""
Evaluation harness with known-geography fixtures.
Tests structural correctness and plausibility of outputs.
Run with: python tests/eval_test.py
Requires the server to be running: uvicorn app.main:app --port 8000
"""
import json
import sys
import httpx

BASE_URL = "http://localhost:8000"
TIMEOUT = 180.0

# Known-geography fixtures with expected output ranges
FIXTURES = [
    {
        "name": "high_competition_urban (Shoreditch cafe)",
        "description": "Dense urban area with many cafes — expect high competition, lower location score",
        "request": {
            "address": "Shoreditch High Street, London, UK",
            "business_type": "cafe",
            "radius_meters": 500,
            "max_competitors": 15,
        },
        "assertions": {
            "min_competitors": 3,
            "max_location_score": 70.0,
            "min_gaps": 0,
            "summary_min_length": 50,
            "valid_footfall_values": ["low", "medium", "high"],
        },
    },
    {
        "name": "moderate_competition (Canary Wharf restaurant)",
        "description": "Business district with office lunch trade — expect moderate competition",
        "request": {
            "address": "Canary Wharf, London, UK",
            "business_type": "restaurant",
            "radius_meters": 800,
            "max_competitors": 20,
        },
        "assertions": {
            "min_competitors": 2,
            "min_location_score": 30.0,
            "min_gaps": 0,
            "summary_min_length": 50,
            "valid_footfall_values": ["low", "medium", "high"],
        },
    },
]


def evaluate_fixture(fixture: dict) -> bool:
    name = fixture["name"]
    print(f"\n--- Eval: {name} ---")
    print(f"  {fixture['description']}")

    try:
        r = httpx.post(f"{BASE_URL}/research", json=fixture["request"], timeout=TIMEOUT)
    except httpx.ConnectError:
        print("  [ERROR] Could not connect to server. Is it running on port 8000?")
        return False

    if r.status_code != 200:
        print(f"  [FAIL] HTTP {r.status_code}: {r.text[:300]}")
        return False

    data = r.json()
    a = fixture["assertions"]
    passed = True

    # Competitor count
    n_competitors = len(data.get("competitors", []))
    min_c = a.get("min_competitors", 0)
    if n_competitors < min_c:
        print(f"  [FAIL] competitors: got {n_competitors}, expected >= {min_c}")
        passed = False
    else:
        print(f"  [OK] competitors: {n_competitors} (>= {min_c})")

    # Location score range
    loc_score = data.get("location_score", {}).get("overall", -1)
    if "max_location_score" in a and loc_score > a["max_location_score"]:
        print(f"  [FAIL] location_score: {loc_score:.1f} > max {a['max_location_score']}")
        passed = False
    elif "min_location_score" in a and loc_score < a["min_location_score"]:
        print(f"  [FAIL] location_score: {loc_score:.1f} < min {a['min_location_score']}")
        passed = False
    else:
        print(f"  [OK] location_score: {loc_score:.1f}/100")

    # Market gaps
    n_gaps = len(data.get("market_gaps", []))
    min_g = a.get("min_gaps", 0)
    if n_gaps < min_g:
        print(f"  [FAIL] market_gaps: got {n_gaps}, expected >= {min_g}")
        passed = False
    else:
        print(f"  [OK] market_gaps: {n_gaps}")

    # Executive summary length
    summary = data.get("executive_summary", "")
    min_len = a.get("summary_min_length", 0)
    if len(summary) < min_len:
        print(f"  [FAIL] summary too short: {len(summary)} chars (min {min_len})")
        passed = False
    else:
        print(f"  [OK] executive_summary: {len(summary)} chars")

    # Footfall value validity
    footfall = data.get("traffic_estimate", {}).get("estimated_daily_footfall", "")
    valid_vals = a.get("valid_footfall_values", [])
    if valid_vals and footfall not in valid_vals:
        print(f"  [FAIL] footfall '{footfall}' not in {valid_vals}")
        passed = False
    else:
        print(f"  [OK] footfall: {footfall!r}")

    # Recommendations present
    recs = data.get("recommendations", [])
    if not recs:
        print("  [WARN] no recommendations returned")
    else:
        print(f"  [OK] recommendations: {len(recs)}")

    status = "PASS" if passed else "FAIL"
    print(f"  >>> {status}: {name}")
    return passed


if __name__ == "__main__":
    print("=== Market Research Agent — Evaluation Suite ===")

    results = [evaluate_fixture(f) for f in FIXTURES]

    total = len(results)
    passed = sum(results)
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} fixtures passed")

    if passed < total:
        sys.exit(1)
    print("All evaluations passed.")
