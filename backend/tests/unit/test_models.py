import pytest

from app.models.transaction import Transaction
from app.models.user import User

pytestmark = pytest.mark.unit


def test_user_model_persists_and_defaults(db_session):
    user = User(
        username="modeluser",
        email="modeluser@example.com",
        hashed_password="hashed",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.created_at is not None
    assert user.disabled is False


def test_transaction_model_persists_and_defaults(user_factory, db_session):
    user, _ = user_factory(username="txmodel", password="pass1234")
    transaction = Transaction(
        user_id=user.id,
        title="Model Transaction",
        amount=99.5,
        type="income",
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)

    assert transaction.id is not None
    assert transaction.created_at is not None
    assert transaction.date is not None
    assert transaction.category is None
