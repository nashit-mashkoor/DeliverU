from fastapi.testclient import TestClient


def test_openapi_requires_basic_auth(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 401


def test_unknown_route_returns_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
