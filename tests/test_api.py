"""Integration tests for TerraSeek FastAPI endpoints."""

from fastapi.testclient import TestClient

from terraseek.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_list_aois():
    response = client.get("/api/v1/aois")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert "egypt_cairo" in data


def test_investigate_endpoint():
    payload = {
        "query": "Find newly built structures and urban expansion",
        "aoi_name": "Egypt — Greater Cairo & New Administrative Capital",
        "aoi_bbox": [29.5, 31.0, 30.5, 32.5],
        "date_start": "2015-01-01",
        "date_end": "2024-01-01",
    }
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "investigation_id" in data
    assert data["candidate_count"] > 0
    candidate_id = data["candidates"][0]["id"]

    # Retrieve candidate detail
    detail_resp = client.get(f"/api/v1/candidates/{candidate_id}?investigation_id={data['investigation_id']}")
    assert detail_resp.status_code == 200
    detail_data = detail_resp.json()
    assert detail_data["id"] == candidate_id
    assert "quality_checks" in detail_data

    # Submit decision
    decision_payload = {
        "investigation_id": data["investigation_id"],
        "candidate_id": candidate_id,
        "decision": "CONFIRMED",
        "notes": "Verified earthmoving and foundation layout.",
    }
    dec_resp = client.post("/api/v1/decisions", json=decision_payload)
    assert dec_resp.status_code == 200
    assert dec_resp.json()["status"] == "recorded"

    # Export investigation
    export_resp = client.get(f"/api/v1/export/{data['investigation_id']}")
    assert export_resp.status_code == 200
    export_data = export_resp.json()
    assert export_data["investigation_id"] == data["investigation_id"]
    assert candidate_id in export_data["decisions"]


def test_investigate_invalid_dates():
    payload = {
        "query": "Invalid date range query test",
        "aoi_name": "Neom",
        "aoi_bbox": [28.00, 35.15, 28.15, 35.35],
        "date_start": "2024-01-01",
        "date_end": "2021-01-01",  # start after end
    }
    response = client.post("/api/v1/investigate", json=payload)
    assert response.status_code == 422
