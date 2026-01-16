from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models
from ..security import hash_password, verify_password, create_access_token, decode_token


router = APIRouter()

def db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(db_dep),
) -> models.User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing token")

    token = authorization.split(" ", 1)[1]
    sub = decode_token(token)
    if not sub:
        raise HTTPException(401, "Invalid token")

    user = db.query(models.User).filter_by(id=int(sub)).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user


@router.post("/register")
def register(email: str, password: str, full_name: str = "", db: Session = Depends(db_dep)):
    if db.query(models.User).filter_by(email=email).first():
        raise HTTPException(400, "Email already exists")
    u = models.User(email=email, password_hash=hash_password(password), full_name=full_name)
    db.add(u)
    db.commit()
    return {"ok": True}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(db_dep)):
    u = db.query(models.User).filter_by(email=email).first()
    if not u or not verify_password(password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(str(u.id))
    return {"access_token": token, "token_type": "bearer"}
