def test_run_simulation_baseline(client):
    """Test running a what-if scenario with default parameters."""
    payload = {
        "agvCount": 18,
        "orderVolumeChange": 0,
        "closedAisles": []
    }
    response = client.post("/api/v1/simulation/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "before" in data
    assert "after" in data
    assert "risk" in data["after"]
    assert "queue" in data["after"]
    assert "delay" in data["after"]


def test_run_simulation_with_volume_surge(client):
    """Test simulation with 50% order volume surge increases congestion risk."""
    baseline = client.post("/api/v1/simulation/run", json={"agvCount": 18, "orderVolumeChange": 0, "closedAisles": []}).json()
    surge = client.post("/api/v1/simulation/run", json={"agvCount": 18, "orderVolumeChange": 50, "closedAisles": []}).json()

    assert surge["after"]["risk"] >= baseline["after"]["risk"]
    assert surge["after"]["delay"] >= baseline["after"]["delay"]


def test_run_simulation_with_aisle_closure(client):
    """Test simulating aisle closure (maintenance) correctly increases risk and delay."""
    baseline = client.post("/api/v1/simulation/run", json={"agvCount": 18, "orderVolumeChange": 0, "closedAisles": []}).json()
    closure = client.post("/api/v1/simulation/run", json={"agvCount": 18, "orderVolumeChange": 0, "closedAisles": ["AISLE-B"]}).json()

    assert closure["after"]["risk"] > baseline["after"]["risk"]


def test_get_saved_scenarios(client):
    """Test retrieving saved what-if scenario templates."""
    response = client.get("/api/v1/simulation/scenarios")
    assert response.status_code == 200
    scenarios = response.json()
    assert isinstance(scenarios, list)
