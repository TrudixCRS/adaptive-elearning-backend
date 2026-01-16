from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models

router = APIRouter()

@router.get("/{lesson_id}")
def get_lesson_by_id(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "title": lesson.title,
        "lesson_type": lesson.lesson_type,
        "difficulty": lesson.difficulty,
        "content": lesson.content or "",
        "sort_order": lesson.sort_order,
    }
