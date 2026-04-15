import pytest

pytestmark = pytest.mark.integration

def test_register_success(client):
    response = client.post(
        "/auth/register",
        data={"username": "newuser", "password": "newpass123"},
    )

    body = response.json()
    assert response.status_code == 201
    assert body["message"] == "User registered successfully"
    assert "user_id" in body


def test_register_duplicate_user_fails(client):
    payload = {"username": "dupuser", "password": "pass1234"}
    first = client.post("/auth/register", data=payload)
    second = client.post("/auth/register", data=payload)

    assert first.status_code == 201
    assert second.status_code == 400
    assert second.json()["detail"] == "Username or email already registered"


def test_login_success_returns_bearer_token(client):
    client.post("/auth/register", data={"username": "loginok", "password": "pass1234"})

    response = client.post("/auth/login", data={"username": "loginok", "password": "pass1234"})

    body = response.json()
    assert response.status_code == 200
    assert body["token_type"] == "bearer"
    assert "access_token" in body


def test_login_invalid_credentials(client):
    client.post("/auth/register", data={"username": "loginbad", "password": "pass1234"})

    response = client.post("/auth/login", data={"username": "loginbad", "password": "wrongpass"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_protected_route_requires_auth(client):
    response = client.get("/transactions/")

    assert response.status_code == 401


def test_protected_route_works_with_auth_token(client):
    client.post("/auth/register", data={"username": "authok", "password": "pass1234"})
    login = client.post("/auth/login", data={"username": "authok", "password": "pass1234"})
    token = login.json()["access_token"]

    response = client.get("/transactions/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == []
