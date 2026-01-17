from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from . import models

def require_admin(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    if getattr(user, "role", "student") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only",
        )
    return user