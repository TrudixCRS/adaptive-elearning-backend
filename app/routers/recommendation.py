from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from sqlalchemy import asc

from ..db import SessionLocal
from .. import models
from ..security import decode_token
from ..recommender import score_candidate

router = APIRouter()

def db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id_from_auth(auth: str | None) -> int:
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(401, "Missing token")
    token = auth.split(" ", 1)[1]
    sub = decode_token(token)
    if not sub:
        raise HTTPException(401, "Invalid token")
    return int(sub)

@router.get("/next")
def next_lesson(
    course_id: int,
    mode: str = Query("adaptive", pattern="^(adaptive|baseline)$"),
    authorization: str | None = Header(default=None),
    db: Session = Depends(db_dep),
):
    user_id = get_user_id_from_auth(authorization)

    prefs = db.query(models.UserPreferences).filter_by(user_id=user_id).first()
    if not prefs:
        prefs = models.UserPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    lessons = (
        db.query(models.Lesson)
        .join(models.Module, models.Module.id == models.Lesson.module_id)
        .filter(models.Module.course_id == course_id)
        .order_by(asc(models.Module.sort_order), asc(models.Lesson.sort_order))
        .all()
    )
    if not lessons:
        raise HTTPException(404, "No lessons found")

    prog_rows = db.query(models.Progress).filter_by(user_id=user_id).all()
    prog = {p.lesson_id: p for p in prog_rows}

    if mode == "baseline":
        for L in lessons:
            p = prog.get(L.id)
            if not p or getattr(p, "status", None) != "completed":
                return {
                    "lesson_id": L.id,
                    "title": L.title,
                    "lesson_type": L.lesson_type,
                    "difficulty": L.difficulty,
                    "reason": "Baseline: fixed order.",
                }
        raise HTTPException(404, "All lessons completed")

    def pref_weight(lesson_type: str) -> float:
        lt = (lesson_type or "").lower()
        return float({
            "text": getattr(prefs, "prefer_text", 0.25),
            "video": getattr(prefs, "prefer_video", 0.25),
            "interactive": getattr(prefs, "prefer_interactive", 0.25),
            "quiz": getattr(prefs, "prefer_quiz", 0.25),
        }.get(lt, 0.25))

    best = None
    for L in lessons:
        p = prog.get(L.id)
        if p and getattr(p, "status", None) == "completed":
            continue

        mastery = float(getattr(p, "mastery", 0.0) or 0.0) if p else 0.0
        attempts = int(getattr(p, "attempts", 0) or 0) if p else 0

        s, r = score_candidate(mastery, attempts, pref_weight(L.lesson_type), L.difficulty)
        if best is None or s > best[0]:
            best = (s, r, L)

    if not best:
        raise HTTPException(404, "No candidate lesson")

    s, r, L = best
    return {
        "lesson_id": L.id,
        "title": L.title,
        "lesson_type": L.lesson_type,
        "difficulty": L.difficulty,
        "reason": f"Adaptive: {r}",
        "score": s,
    }
