from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.RoleEnum.viewer:
        raise HTTPException(status_code=403, detail="Viewers cannot create transactions")
    db_transaction = models.Transaction(**transaction.dict(), user_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[schemas.TransactionOut])
def get_transactions(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    )
    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    return query.all()

@router.get("/{transaction_id}", response_model=schemas.TransactionOut)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(
    transaction_id: int,
    updated: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.RoleEnum.viewer:
        raise HTTPException(status_code=403, detail="Viewers cannot update transactions")
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.RoleEnum.viewer:
        raise HTTPException(status_code=403, detail="Viewers cannot delete transactions")
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}