from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models import RoleEnum

# --- User schemas ---
class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[RoleEnum] = RoleEnum.viewer

class UserOut(BaseModel):
    id: int
    email: str
    role: RoleEnum

    class Config:
        orm_mode = True

# --- Token schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Transaction schemas ---
class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str] = None

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str]
    user_id: int

    class Config:
        orm_mode = True