def test_root_endpoint(client):
    """Test the root endpoint returns online status and system name."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Online"
    assert "TwinFlow" in data["system"]
    assert data["apiDocs"] == "/docs"
    assert data["version"] == "1.0.0"


def test_health_endpoint(client):
    """Test health check endpoint reports healthy database and pipeline."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Healthy"
    assert data["database"] == "Connected"
    assert data["pipeline"] == "Active"


def test_nonexistent_route_returns_404(client):
    """Test accessing an unknown path returns 404."""
    response = client.get("/api/v1/invalid-route-xyz")
    assert response.status_code == 404
