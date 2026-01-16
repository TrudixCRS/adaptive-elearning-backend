from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc
from ..db import SessionLocal
from .. import models

router = APIRouter()

def db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(db_dep)):
    course = db.query(models.Course).filter_by(id=course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")

    modules = (
        db.query(models.Module)
        .filter_by(course_id=course_id)
        .order_by(asc(models.Module.sort_order))
        .all()
    )

    module_ids = [m.id for m in modules]
    lessons = []
    if module_ids:
        lessons = (
            db.query(models.Lesson)
            .filter(models.Lesson.module_id.in_(module_ids))
            .order_by(asc(models.Lesson.module_id), asc(models.Lesson.sort_order))
            .all()
        )

    # group lessons by module
    by_module = {}
    for L in lessons:
        by_module.setdefault(L.module_id, []).append({
            "id": L.id,
            "title": L.title,
            "lesson_type": L.lesson_type,
            "difficulty": L.difficulty,
            "sort_order": L.sort_order
        })

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "modules": [
            {
                "id": m.id,
                "title": m.title,
                "sort_order": m.sort_order,
                "lessons": by_module.get(m.id, [])
            }
            for m in modules
        ]
    }
