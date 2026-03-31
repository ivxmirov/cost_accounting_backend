from decimal import Decimal

from app.models import User, Wallet


def test_add_expense_success(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Expense has been added."
    assert response.json()["wallet"] == wallet.name
    assert Decimal(str(response.json()["amount"])) == Decimal(50)
    assert Decimal(str(response.json()["new_balance"])) == Decimal(150)
    assert response.json()["description"] == "food"


def test_add_expense_negative_amount(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -100.0,
            "description": "food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 422


def test_add_expense_empty_name(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "     ",
            "amount": 100.0,
            "description": "food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 422


def test_add_expense_wallet_not_exists(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 404


def test_add_expense_unauthorized(client):
    # Arrange

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 100.0,
            "description": "food",
        },
        headers={"Authorization": "Bearer not_exists"},
    )

    # Assert
    assert response.status_code == 401


def test_add_expense_not_enough_money(db_session, client):
    # Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    # Act
    response = client.post(
        "api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 1000.00,
            "description": "food",
        },
        headers={"Authorization": f"Bearer {user.login}"},
    )

    # Assert
    assert response.status_code == 400
