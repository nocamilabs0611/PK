def test_get_analytics_metrics(client):
    """Test retrieving high-level analytics KPIs and trend charts."""
    response = client.get("/api/v1/analytics/metrics?range=7d&zone=All%20Zones")
    assert response.status_code == 200
    data = response.json()
    assert "predictionAccuracy" in data
    assert data["predictionAccuracy"] >= 90.0
    assert "avgLeadTimeMin" in data
    assert "bottlenecksPrevented" in data
    assert "chartData" in data
    assert "congestionTrend" in data["chartData"]


def test_get_and_create_audit_logs(client):
    """Test creating an audit log and retrieving audit history."""
    new_log = {
        "user": "operator.sam",
        "action": "Triggered manual reroute simulation for Zone 2",
        "module": "Simulation",
        "time": "11:45",
        "ip": "192.168.1.42"
    }
    create_res = client.post("/api/v1/audit/logs", json=new_log)
    assert create_res.status_code == 200
    assert create_res.json()["success"] is True

    # Retrieve logs
    get_res = client.get("/api/v1/audit/logs")
    assert get_res.status_code == 200
    logs = get_res.json()
    assert isinstance(logs, list)
    assert len(logs) >= 1
    actions = [l["action"] for l in logs]
    assert any("Triggered manual reroute simulation" in a for a in actions)
