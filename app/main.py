from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, courses, recommendation, course_detail, lesson_detail, progress, lessons

from .db import SessionLocal
from .seed import run_seed
from .models import Course

app = FastAPI(title="Adaptive E-Learning API", redirect_slashes=False)
app.security = [HTTPBearer()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://adaptive-elearning-frontend.vercel.app",
        "https://adaptive-learning.co.uk",
        "https://www.adaptive-learning.co.uk",
        "https://adaptive-elearning-backend-production.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_seed():
    db = SessionLocal()
    try:
        # Only seed if no courses exist
        if db.query(Course).count() == 0:
            run_seed(db)
            print("✅ Database seeded")
        else:
            print("ℹ️ Seed skipped (data exists)")
    finally:
        db.close()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(recommendation.router, prefix="/recommendation", tags=["recommendation"])
app.include_router(course_detail.router, prefix="/courses", tags=["courses"])
app.include_router(lesson_detail.router, prefix="/lessons", tags=["lessons"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
