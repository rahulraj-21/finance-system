from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, get_db
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.routers import transactions, analytics, admin
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API")

app.include_router(transactions.router)
app.include_router(analytics.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to Finance Tracker API"}

@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user