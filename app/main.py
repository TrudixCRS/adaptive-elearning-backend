from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from .db import Base, engine
from .routers import auth, courses, recommendation
from .routers import course_detail, lesson_detail
from .routers import progress, lessons


app = FastAPI(title="Adaptive E-Learning API")
app.security = [HTTPBearer()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(recommendation.router, prefix="/recommendation", tags=["recommendation"])
app.include_router(course_detail.router, prefix="/courses", tags=["courses"])
app.include_router(lesson_detail.router, prefix="/lessons", tags=["lessons"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
