from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..db import SessionLocal
from .. import models
from ..security import decode_token

router = APIRouter(prefix="/auth", tags=["auth"])
bearer = HTTPBearer(auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = creds.credentials
    sub = decode_token(token)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter_by(email=sub).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {
        "email": user.email,
        "full_name": user.full_name,
        "role": getattr(user, "role", "student"),
    }
