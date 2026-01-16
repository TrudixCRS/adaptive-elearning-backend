from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(db_dep)):
    lesson = db.query(models.Lesson).filter_by(id=lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    return {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "lesson_type": lesson.lesson_type,
        "difficulty": lesson.difficulty,
        "content": lesson.content or ""
    }
