from fastapi import HTTPException

from app.database import SessionLocal
from app.repository import wallets as wallets_repository
from app.schemas import OperationRequest


def add_income(operation: OperationRequest):
    db = SessionLocal()

    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404, detail=f"Wallet <{operation.wallet_name}> not found."
            )

        wallet = wallets_repository.add_income(
            db, operation.wallet_name, operation.amount
        )

        db.commit()

        return {
            "message": "Income has been added.",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.balance,  # type: ignore
        }

    finally:
        db.close()


def add_expense(operation: OperationRequest):
    db = SessionLocal()

    try:
        if not wallets_repository.is_wallet_exist(db, operation.wallet_name):
            raise HTTPException(
                status_code=404, detail=f"Wallet <{operation.wallet_name}> not found."
            )

        wallet = wallets_repository.add_expense(
            db, operation.wallet_name, operation.amount
        )

        if wallet.balance < operation.amount:  # type: ignore

            raise HTTPException(
                status_code=400,
                detail=f"Insufficient funds. Available: {wallet.balance}.",  # type: ignore
            )

        db.commit()

        return {
            "message": "Expense has been added.",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.balance,  # type: ignore
        }

    finally:
        db.close()
