def test_get_warehouse_config(client):
    """Test getting warehouse configuration returns thresholds and aisles."""
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert "thresholds" in data
    assert "aisles" in data
    assert data["thresholds"]["moderate"] == 40
    assert data["thresholds"]["high"] == 70
    assert data["thresholds"]["critical"] == 85
    assert len(data["aisles"]) >= 4


def test_update_warehouse_thresholds(client):
    """Test updating congestion risk thresholds."""
    update_payload = {
        "thresholds": {
            "moderate": 45,
            "high": 75,
            "critical": 90
        }
    }
    response = client.put("/api/v1/config", json=update_payload)
    assert response.status_code == 200

    # Verify update
    get_res = client.get("/api/v1/config")
    thresholds = get_res.json()["thresholds"]
    assert thresholds["moderate"] == 45
    assert thresholds["high"] == 75
    assert thresholds["critical"] == 90


def test_update_aisle_settings(client):
    """Test modifying aisle name, capacity, and operational status."""
    update_payload = {
        "aisles": [
            {
                "id": "AISLE-A",
                "name": "Aisle A - Modified",
                "capacity": 140,
                "status": "Maintenance"
            }
        ]
    }
    response = client.put("/api/v1/config", json=update_payload)
    assert response.status_code == 200

    # Verify aisle was updated
    get_res = client.get("/api/v1/config")
    aisles = get_res.json()["aisles"]
    aisle_a = next((a for a in aisles if a["id"] == "AISLE-A"), None)
    assert aisle_a is not None
    assert aisle_a["name"] == "Aisle A - Modified"
    assert aisle_a["capacity"] == 140
    assert aisle_a["status"] == "Maintenance"
