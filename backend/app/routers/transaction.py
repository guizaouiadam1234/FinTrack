from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.services.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

# --- Schemas ---
class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str  # "income" or "expense"
    category: str | None = None
    date: datetime | None = None

class TransactionUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    type: str | None = None
    category: str | None = None
    date: datetime | None = None

class SummaryResponse(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    transaction_count: int

class RecentTransactionItem(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str | None = None
    date: datetime

    class Config:
        from_attributes = True

# --- Routes ---
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = Transaction(
        user_id=current_user.id,
        title=data.title,
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date or datetime.utcnow()
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.get("/")
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

@router.get("/summary", response_model=SummaryResponse)
def get_dashboard_summary(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_income = db.query(
        func.coalesce(
            func.sum(case((Transaction.type == "income", Transaction.amount), else_=0.0)),
            0.0,
        )
    ).filter(Transaction.user_id == current_user.id).scalar()

    total_expenses = db.query(
        func.coalesce(
            func.sum(case((Transaction.type == "expense", Transaction.amount), else_=0.0)),
            0.0,
        )
    ).filter(Transaction.user_id == current_user.id).scalar()

    now = datetime.utcnow()
    if start_date is None or end_date is None:
        month_start = datetime(now.year, now.month, 1)
        if now.month == 12:
            month_end = datetime(now.year + 1, 1, 1) - timedelta(microseconds=1)
        else:
            month_end = datetime(now.year, now.month + 1, 1) - timedelta(microseconds=1)
    else:
        month_start = start_date
        month_end = end_date

    monthly_income = db.query(
        func.coalesce(
            func.sum(case((Transaction.type == "income", Transaction.amount), else_=0.0)),
            0.0,
        )
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= month_start,
        Transaction.date <= month_end,
    ).scalar()

    monthly_expenses = db.query(
        func.coalesce(
            func.sum(case((Transaction.type == "expense", Transaction.amount), else_=0.0)),
            0.0,
        )
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= month_start,
        Transaction.date <= month_end,
    ).scalar()

    transaction_count = db.query(func.count(Transaction.id)).filter(Transaction.user_id == current_user.id).scalar()

    return SummaryResponse(
        total_balance=float(total_income - total_expenses),
        monthly_income=float(monthly_income),
        monthly_expenses=float(monthly_expenses),
        transaction_count=int(transaction_count or 0),
    )

@router.get("/recent", response_model=list[RecentTransactionItem])
def get_recent_transactions(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    safe_limit = min(max(limit, 1), 100)
    return db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(
        Transaction.date.desc(),
        Transaction.id.desc(),
    ).limit(safe_limit).all()

@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}")
def update_transaction(transaction_id: int, data: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()

@router.get("/sorted")
def get_sorted_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.date.desc()).all()