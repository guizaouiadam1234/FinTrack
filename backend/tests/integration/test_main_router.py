import pytest

pytestmark = pytest.mark.integration

def test_root_health_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FinTrack API"}
