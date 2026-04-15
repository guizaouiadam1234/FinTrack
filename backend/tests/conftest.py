import os
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure env vars exist before importing app modules.
os.environ.setdefault("DATABASE_URL", "sqlite:///./tests_bootstrap.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.database import Base, get_db  # noqa: E402
from app.models.transaction import Transaction  # noqa: E402
from app.models.user import User  # noqa: E402
from app.services.auth import create_access_token, hash_password  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def user_factory(db_session):
    def _create_user(username="tester", password="pass1234"):
        user = User(
            username=username,
            email=f"{username}@example.com",
            hashed_password=hash_password(password),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user, password

    return _create_user


@pytest.fixture()
def auth_headers(user_factory):
    def _headers(username="tester", password="pass1234"):
        user, _ = user_factory(username=username, password=password)
        token = create_access_token({"sub": user.username})
        return {"Authorization": f"Bearer {token}"}, user

    return _headers


@pytest.fixture()
def transaction_factory(db_session):
    def _create_transaction(
        user_id,
        title="Sample",
        amount=10.0,
        tx_type="expense",
        category="General",
        date=None,
    ):
        transaction = Transaction(
            user_id=user_id,
            title=title,
            amount=amount,
            type=tx_type,
            category=category,
            date=date or datetime.utcnow(),
        )
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)
        return transaction

    return _create_transaction
