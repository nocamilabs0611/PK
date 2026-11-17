def test_get_live_predictions(client):
    """Test DSTGT model live prediction endpoint returns required heads and explainability."""
    response = client.get("/api/v1/predictions/live")
    assert response.status_code == 200
    data = response.json()

    # Core predictions
    assert "congestionProbability" in data
    assert 0 <= data["congestionProbability"] <= 100
    assert "bottleneckLocation" in data
    assert "queueLength" in data
    assert data["queueHorizonMin"] == 15
    assert "delayTime" in data
    assert "confidence" in data
    assert "riskLabel" in data

    # Explainable AI features
    assert "influentialFeatures" in data
    features = data["influentialFeatures"]
    assert len(features) >= 3
    for f in features:
        assert "name" in f
        assert "weight" in f
        assert 0 <= f["weight"] <= 1.0

    # Model metadata
    assert "modelInfo" in data
    model = data["modelInfo"]
    assert model["name"] == "DSTGT v1.0"
    assert "accuracy" in model
    assert model["accuracy"] > 80.0


def test_retrain_model(client):
    """Test triggering DSTGT model retraining starts asynchronous training job."""
    response = client.post("/api/v1/predictions/retrain")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "jobId" in data
    assert data["status"] == "Started"
    assert data["etaSeconds"] > 0
