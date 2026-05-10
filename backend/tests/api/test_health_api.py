from fastapi.testclient import TestClient

def test_health_check(client: TestClient):
    """
    Validates that the health check API is returning a 200 OK
    and the correct operational status.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
