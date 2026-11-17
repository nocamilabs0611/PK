def test_get_reports_list(client):
    """Test retrieving list of generated enterprise reports."""
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    reports = response.json()
    assert isinstance(reports, list)


def test_create_report_csv(client):
    """Test requesting a new CSV report generation."""
    payload = {
        "type": "Congestion Incident Summary",
        "dateRange": "Last 7 Days",
        "format": "csv",
        "createdBy": "Test Admin",
        "customReportName": "Test Congestion Analysis CSV"
    }
    response = client.post("/api/v1/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "reportId" in data
    assert data["status"] == "Generating"


def test_download_report_not_found(client):
    """Test requesting non-existent report returns 404."""
    response = client.get("/api/v1/reports/NONEXISTENT-REPORT/download")
    assert response.status_code == 404
