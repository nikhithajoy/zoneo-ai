"""
Integration smoke test — no test framework, just direct HTTP calls.
Run with: python tests/integration_test.py
Requires the server to be running: uvicorn app.main:app --port 8000
"""
import json
import sys
import httpx

BASE_URL = "http://localhost:8000"
TIMEOUT = 180.0  # pipeline can take 2-3 minutes


def test_health():
    r = httpx.get(f"{BASE_URL}/health")
    assert r.status_code == 200, f"Health check failed: {r.status_code}"
    assert r.json()["status"] == "ok"
    print("  [PASS] /health")


def test_research():
    payload = {
        "address": "Shoreditch High Street, London, UK",
        "business_type": "cafe",
        "radius_meters": 800,
        "max_competitors": 10,
    }
    print(f"\n  Request: {json.dumps(payload, indent=4)}")

    r = httpx.post(f"{BASE_URL}/research", json=payload, timeout=TIMEOUT)
    assert r.status_code == 200, f"Research failed: {r.status_code}\n{r.text[:500]}"

    data = r.json()

    # Structural assertions
    assert "executive_summary" in data and len(data["executive_summary"]) > 20
    assert isinstance(data["competitors"], list)
    assert "location_score" in data
    assert "overall" in data["location_score"]
    assert isinstance(data["market_gaps"], list)
    assert isinstance(data["recommendations"], list)

    print(f"  Executive summary: {data['executive_summary'][:150]}...")
    print(f"  Competitors found: {len(data['competitors'])}")
    print(f"  Location score:    {data['location_score']['overall']:.1f}/100")
    print(f"  Traffic estimate:  {data['traffic_estimate']['estimated_daily_footfall']}")
    print(f"  Market gaps:       {len(data['market_gaps'])}")
    print(f"  Recommendations:   {len(data['recommendations'])}")
    print("  [PASS] POST /research")
    return data


if __name__ == "__main__":
    print("=== Market Research Agent — Integration Test ===\n")
    try:
        test_health()
        test_research()
        print("\nAll tests passed.")
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except httpx.ConnectError:
        print("\n[ERROR] Could not connect to server. Is it running on port 8000?")
        print("  Start with: uvicorn app.main:app --reload --port 8000")
        sys.exit(1)
