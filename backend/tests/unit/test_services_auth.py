from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from app.services import auth as auth_service

pytestmark = pytest.mark.unit


def test_hash_and_verify_password_roundtrip():
    password = "my-secret-password"
    hashed = auth_service.hash_password(password)

    assert hashed != password
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrong-password", hashed)


def test_create_access_token_default_expiry_and_claims():
    token = auth_service.create_access_token({"sub": "alice"})
    payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])

    assert payload["sub"] == "alice"
    assert "exp" in payload


def test_create_access_token_with_custom_expiry():
    token = auth_service.create_access_token({"sub": "bob"}, expires_delta=timedelta(minutes=2))
    payload = jwt.decode(token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])

    assert payload["sub"] == "bob"
    assert "exp" in payload


def test_get_user_by_username_found_and_not_found(user_factory, db_session):
    user, _ = user_factory(username="carol", password="pass1234")

    found = auth_service.get_user_by_username(db_session, "carol")
    missing = auth_service.get_user_by_username(db_session, "nobody")

    assert found is not None
    assert found.id == user.id
    assert missing is None


def test_authenticate_user_success_and_failure(user_factory, db_session):
    user_factory(username="dave", password="validpass")

    ok = auth_service.authenticate_user(db_session, "dave", "validpass")
    bad_password = auth_service.authenticate_user(db_session, "dave", "invalid")
    bad_user = auth_service.authenticate_user(db_session, "unknown", "validpass")

    assert ok is not None
    assert ok.username == "dave"
    assert bad_password is None
    assert bad_user is None


def test_get_current_user_invalid_token_raises(db_session):
    with pytest.raises(HTTPException) as exc:
        auth_service.get_current_user("not-a-token", db_session)

    assert exc.value.status_code == 401


def test_get_current_user_missing_sub_raises(db_session):
    token = auth_service.create_access_token({"role": "user"})

    with pytest.raises(HTTPException) as exc:
        auth_service.get_current_user(token, db_session)

    assert exc.value.status_code == 401


def test_get_current_user_user_not_found_raises(db_session):
    token = auth_service.create_access_token({"sub": "ghost"})

    with pytest.raises(HTTPException) as exc:
        auth_service.get_current_user(token, db_session)

    assert exc.value.status_code == 401


def test_get_current_user_success(user_factory, db_session):
    user, _ = user_factory(username="eve", password="pass1234")
    token = auth_service.create_access_token({"sub": "eve"})

    current_user = auth_service.get_current_user(token, db_session)

    assert current_user.id == user.id
    assert current_user.username == "eve"
