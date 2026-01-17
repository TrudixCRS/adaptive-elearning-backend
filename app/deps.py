from fastapi import Depends, HTTPException, status
from .security import get_current_user


def require_admin(user=Depends(get_current_user)):
    if getattr(user, "role", None) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user
