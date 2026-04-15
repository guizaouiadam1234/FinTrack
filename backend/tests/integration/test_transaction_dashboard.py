from datetime import datetime, timedelta, timezone

import pytest

pytestmark = pytest.mark.integration


def _login_token(client, username):
    client.post("/auth/register", data={"username": username, "password": "pass1234"})
    login = client.post("/auth/login", data={"username": username, "password": "pass1234"})
    return login.json()["access_token"]


def _create_transaction(client, token, title, amount, tx_type, date, category="General"):
    return client.post(
        "/transactions/",
        json={
            "title": title,
            "amount": amount,
            "type": tx_type,
            "category": category,
            "date": date.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )


def test_summary_returns_zeros_when_no_transactions(client):
    token = _login_token(client, "summaryempty")

    response = client.get("/transactions/summary", headers={"Authorization": f"Bearer {token}"})

    body = response.json()
    assert response.status_code == 200
    assert body["total_balance"] == 0.0
    assert body["monthly_income"] == 0.0
    assert body["monthly_expenses"] == 0.0
    assert body["transaction_count"] == 0


def test_summary_mixed_data_and_date_window(client):
    token = _login_token(client, "summarymixed")

    now = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1)
    prev_month_mid = (month_start - timedelta(days=1)).replace(day=15)

    _create_transaction(client, token, "Salary", 3000, "income", now)
    _create_transaction(client, token, "Rent", 1200, "expense", now)
    _create_transaction(client, token, "Old Bonus", 500, "income", prev_month_mid)

    default_summary = client.get("/transactions/summary", headers={"Authorization": f"Bearer {token}"})
    default_body = default_summary.json()

    assert default_summary.status_code == 200
    assert default_body["total_balance"] == 2300.0
    assert default_body["monthly_income"] == 3000.0
    assert default_body["monthly_expenses"] == 1200.0
    assert default_body["transaction_count"] == 3

    prev_start = prev_month_mid.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    prev_end = month_start - timedelta(microseconds=1)
    ranged = client.get(
        "/transactions/summary",
        params={
            "start_date": prev_start.isoformat(),
            "end_date": prev_end.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    ranged_body = ranged.json()
    assert ranged.status_code == 200
    assert ranged_body["monthly_income"] == 500.0
    assert ranged_body["monthly_expenses"] == 0.0


def test_recent_default_limit_and_ordering(client):
    token = _login_token(client, "recentdefault")

    base = datetime.now(timezone.utc).replace(hour=11, minute=0, second=0, microsecond=0)
    for index in range(25):
        date = base + timedelta(minutes=index)
        _create_transaction(client, token, f"Tx {index}", index + 1, "expense", date)

    response = client.get("/transactions/recent", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 20
    assert body[0]["title"] == "Tx 24"
    assert body[-1]["title"] == "Tx 5"


def test_recent_limit_clamping_low_and_high(client):
    token = _login_token(client, "recentclamp")

    same_date = datetime.now(timezone.utc).replace(hour=9, minute=0, second=0, microsecond=0)
    for index in range(105):
        _create_transaction(client, token, f"Item {index}", 1, "expense", same_date)

    low = client.get("/transactions/recent", params={"limit": 0}, headers={"Authorization": f"Bearer {token}"})
    high = client.get("/transactions/recent", params={"limit": 500}, headers={"Authorization": f"Bearer {token}"})

    assert low.status_code == 200
    assert len(low.json()) == 1

    high_body = high.json()
    assert high.status_code == 200
    assert len(high_body) == 100

    # Same date for all rows means ordering falls back to id desc.
    assert high_body[0]["title"] == "Item 104"
