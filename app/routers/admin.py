from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import require_admin
from .. import models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    users = db.query(models.User).count()
    courses = db.query(models.Course).count()
    return {"users": users, "courses": courses}

@router.get("/users")
def list_users(db: Session = Depends(get_db), _=Depends(require_admin)):
    items = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return [
        {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role, "created_at": u.created_at}
        for u in items
    ]

@router.patch("/users/{user_id}/role")
def set_role(user_id: int, role: str, db: Session = Depends(get_db), _=Depends(require_admin)):
    if role not in ("student", "admin"):
        raise HTTPException(400, "role must be student or admin")
    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u:
        raise HTTPException(404, "User not found")
    u.role = role
    db.commit()
    return {"ok": True}

@router.post("/courses")
def create_course(title: str, description: str, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = models.Course(title=title, description=description)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "title": c.title, "description": c.description}

@router.put("/courses/{course_id}")
def update_course(course_id: int, title: str, description: str, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c:
        raise HTTPException(404, "Course not found")
    c.title = title
    c.description = description
    db.commit()
    return {"ok": True}

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not c:
        raise HTTPException(404, "Course not found")
    db.delete(c)
    db.commit()
    return {"ok": True}
