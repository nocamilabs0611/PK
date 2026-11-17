def test_get_alerts(client):
    """Test retrieving list of bottleneck tripwire alerts."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert isinstance(alerts, list)
    assert len(alerts) >= 1
    sample = alerts[0]
    assert "id" in sample
    assert "severity" in sample
    assert "title" in sample
    assert "status" in sample


def test_acknowledge_alert(client):
    """Test acknowledging an active bottleneck alert."""
    response = client.post("/api/v1/alerts/ALT-101/acknowledge")
    assert response.status_code == 200
    assert response.json()["status"] == "Acknowledged"

    # Verify status changed in list
    list_res = client.get("/api/v1/alerts")
    alert = next((a for a in list_res.json() if a["id"] == "ALT-101"), None)
    assert alert is not None
    assert alert["status"] == "Acknowledged"


def test_resolve_alert(client):
    """Test resolving an active bottleneck alert."""
    response = client.post("/api/v1/alerts/ALT-101/resolve")
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"


def test_delete_alert(client):
    """Test deleting an alert removes it from the queue."""
    response = client.delete("/api/v1/alerts/ALT-101")
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Verify alert is gone
    get_res = client.delete("/api/v1/alerts/ALT-101")
    assert get_res.status_code == 404


def test_alert_not_found(client):
    """Test acknowledging or resolving a nonexistent alert returns 404."""
    ack_res = client.post("/api/v1/alerts/NONEXISTENT-999/acknowledge")
    assert ack_res.status_code == 404

    res_res = client.post("/api/v1/alerts/NONEXISTENT-999/resolve")
    assert res_res.status_code == 404
