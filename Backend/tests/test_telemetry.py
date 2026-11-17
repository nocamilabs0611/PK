def test_get_live_telemetry_stats(client):
    """Test live telemetry stats endpoint returns active AGVs and broker health."""
    response = client.get("/api/v1/telemetry/live")
    assert response.status_code == 200
    data = response.json()
    assert "activeAgvs" in data
    assert "totalAgvs" in data
    assert "kafkaPipelineStatus" in data
    assert data["kafkaPipelineStatus"] in ["Connected", "Degraded", "Reconnecting"]
    assert data["fps"] >= 30
