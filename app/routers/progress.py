from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json

from ..db import SessionLocal
from .. import models
from .auth import get_current_user

router = APIRouter()

def db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _get_or_create_progress(db: Session, user_id: int, lesson_id: int):
    p = db.query(models.Progress).filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if p:
        return p
    p = models.Progress(user_id=user_id, lesson_id=lesson_id, status="in_progress")
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.post("/complete")
def mark_completed(
    lesson_id: int,
    score: float | None = None,
    db: Session = Depends(db_dep),
    user: models.User = Depends(get_current_user),
):
    lesson = db.query(models.Lesson).filter_by(id=lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    p = db.query(models.Progress).filter_by(user_id=user.id, lesson_id=lesson_id).first()
    if p:
        p.status = "completed"
        if score is not None:
            p.score = score        # ✅ save score on update
        db.commit()
        return {"ok": True, "status": p.status, "score": p.score}

    p = models.Progress(user_id=user.id, lesson_id=lesson_id, status="completed", score=score)  # ✅ save score on insert
    db.add(p)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        p = db.query(models.Progress).filter_by(user_id=user.id, lesson_id=lesson_id).first()
        if p:
            p.status = "completed"
            if score is not None:
                p.score = score
            db.commit()
            return {"ok": True, "status": p.status, "score": p.score}
        raise

    return {"ok": True, "status": p.status, "score": p.score}


@router.get("/me")
def my_progress(
    db: Session = Depends(db_dep),
    user: models.User = Depends(get_current_user),
):
    rows = db.query(models.Progress).filter_by(user_id=user.id).all()
    return [
        {
            "lesson_id": r.lesson_id,
            "status": getattr(r, "status", None),
            "score": getattr(r, "score", None),
            "attempts": getattr(r, "attempts", None),
            "mastery": getattr(r, "mastery", None),
            "updated_at": str(getattr(r, "updated_at", "")),
        }
        for r in rows
    ]

@router.post("/quiz/submit")
def submit_quiz(
    lesson_id: int,
    answers: dict,  # {"q1": 1, "q2": 0, ...} (choice index per question)
    db: Session = Depends(db_dep),
    user: models.User = Depends(get_current_user),
):
    lesson = db.query(models.Lesson).filter_by(id=lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    if (lesson.lesson_type or "").lower() != "quiz":
        raise HTTPException(400, "This lesson is not a quiz")

    # content must be JSON with "questions"
    try:
        payload = json.loads(lesson.content or "{}")
        questions = payload.get("questions", [])
        passing = float(payload.get("passingScore", 0.7))
    except Exception:
        raise HTTPException(400, "Quiz content is not valid JSON")

    if not questions:
        raise HTTPException(400, "Quiz has no questions")

    correct = 0
    total = 0
    for q in questions:
        qid = q.get("id")
        ans_index = q.get("answerIndex")
        if qid is None or ans_index is None:
            continue
        total += 1
        user_ans = answers.get(qid, None)
        if user_ans is not None and int(user_ans) == int(ans_index):
            correct += 1

    score = (correct / total) if total else 0.0

    p = _get_or_create_progress(db, user.id, lesson_id)

    # increment attempts if field exists
    if hasattr(p, "attempts"):
        p.attempts = int(getattr(p, "attempts") or 0) + 1

    # store score if field exists
    if hasattr(p, "score"):
        p.score = float(score)

    # update mastery if field exists
    # simple: mastery nudges toward score, capped 0..1
    if hasattr(p, "mastery"):
        old = float(getattr(p, "mastery") or 0.0)
        new = max(0.0, min(1.0, (old * 0.6) + (score * 0.4)))
        p.mastery = new

    # pass/fail -> status
    p.status = "completed" if score >= passing else "in_progress"

    db.commit()

    return {
        "ok": True,
        "lesson_id": lesson_id,
        "correct": correct,
        "total": total,
        "score": score,
        "status": p.status,
        "mastery": float(getattr(p, "mastery", 0.0) or 0.0),
        "attempts": int(getattr(p, "attempts", 0) or 0),
        "passingScore": passing,
    }
