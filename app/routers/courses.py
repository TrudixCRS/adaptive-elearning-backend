from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import SessionLocal
from .. import models

router = APIRouter()

def db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def list_courses(db: Session = Depends(db_dep)):
    rows = db.query(models.Course).all()
    return [{"id": c.id, "title": c.title, "description": c.description} for c in rows]

