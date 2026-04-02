from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.database import get_db
from app.auth import get_current_user, require_analyst

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "total_transactions": len(transactions)
    }

@router.get("/categories")
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_analyst)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).all()

    breakdown = {}
    for t in transactions:
        if t.category not in breakdown:
            breakdown[t.category] = 0
        breakdown[t.category] += t.amount

    return breakdown

@router.get("/monthly")
def get_monthly_totals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_analyst)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).all()

    monthly = {}
    for t in transactions:
        key = t.date.strftime("%Y-%m")
        if key not in monthly:
            monthly[key] = {"income": 0, "expense": 0}
        monthly[key][t.type] += t.amount

    return monthly

@router.get("/recent")
def get_recent_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    ).order_by(models.Transaction.date.desc()).limit(5).all()

    return transactions