from datetime import datetime, timezone

import pytest

pytestmark = pytest.mark.integration


def _create_transaction(client, token, **overrides):
    payload = {
        "title": "Groceries",
        "amount": 45.25,
        "type": "expense",
        "category": "Food",
        "date": datetime.now(timezone.utc).isoformat(),
    }
    payload.update(overrides)
    return client.post("/transactions/", json=payload, headers={"Authorization": f"Bearer {token}"})


def test_transaction_crud_lifecycle(client):
    client.post("/auth/register", data={"username": "cruduser", "password": "pass1234"})
    login = client.post("/auth/login", data={"username": "cruduser", "password": "pass1234"})
    token = login.json()["access_token"]

    created = _create_transaction(client, token)
    assert created.status_code == 201
    transaction_id = created.json()["id"]

    listed = client.get("/transactions/", headers={"Authorization": f"Bearer {token}"})
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    fetched = client.get(f"/transactions/{transaction_id}", headers={"Authorization": f"Bearer {token}"})
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Groceries"

    updated = client.put(
        f"/transactions/{transaction_id}",
        json={"title": "Groceries Updated", "amount": 60.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Groceries Updated"
    assert updated.json()["amount"] == 60.0

    deleted = client.delete(f"/transactions/{transaction_id}", headers={"Authorization": f"Bearer {token}"})
    assert deleted.status_code == 204

    missing = client.get(f"/transactions/{transaction_id}", headers={"Authorization": f"Bearer {token}"})
    assert missing.status_code == 404


def test_transaction_endpoints_enforce_user_ownership(client):
    client.post("/auth/register", data={"username": "owner", "password": "pass1234"})
    owner_login = client.post("/auth/login", data={"username": "owner", "password": "pass1234"})
    owner_token = owner_login.json()["access_token"]

    created = _create_transaction(client, owner_token, title="Private Tx")
    tx_id = created.json()["id"]

    client.post("/auth/register", data={"username": "other", "password": "pass1234"})
    other_login = client.post("/auth/login", data={"username": "other", "password": "pass1234"})
    other_token = other_login.json()["access_token"]

    get_other = client.get(f"/transactions/{tx_id}", headers={"Authorization": f"Bearer {other_token}"})
    update_other = client.put(
        f"/transactions/{tx_id}",
        json={"title": "Should not update"},
        headers={"Authorization": f"Bearer {other_token}"},
    )
    delete_other = client.delete(f"/transactions/{tx_id}", headers={"Authorization": f"Bearer {other_token}"})

    assert get_other.status_code == 404
    assert update_other.status_code == 404
    assert delete_other.status_code == 404


def test_sorted_transactions_returns_descending_by_date(client):
    client.post("/auth/register", data={"username": "sorter", "password": "pass1234"})
    login = client.post("/auth/login", data={"username": "sorter", "password": "pass1234"})
    token = login.json()["access_token"]

    _create_transaction(client, token, title="Older", date="2026-01-10T10:00:00")
    _create_transaction(client, token, title="Newer", date="2026-02-10T10:00:00")

    response = client.get("/transactions/sorted", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert titles == ["Newer", "Older"]
