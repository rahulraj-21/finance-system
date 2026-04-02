from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.auth import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    return db.query(models.User).all()

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: models.RoleEnum,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    db.commit()
    db.refresh(user)
    return {"message": f"Role updated to {role}"}

@router.get("/transactions", response_model=List[schemas.TransactionOut])
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    return db.query(models.Transaction).all()