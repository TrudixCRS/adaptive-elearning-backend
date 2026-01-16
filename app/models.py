from sqlalchemy import Column, Integer, BigInteger, Text, ForeignKey, Numeric, Boolean, TIMESTAMP, String, Float, DateTime
from datetime import datetime
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(Text)
    role = Column(Text, nullable=False, default="student")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class Course(Base):
    __tablename__ = "courses"
    id = Column(BigInteger, primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class Module(Base):
    __tablename__ = "modules"
    id = Column(BigInteger, primary_key=True)
    course_id = Column(BigInteger, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    lesson_type = Column(Text, nullable=False)  # text|video|interactive|quiz
    difficulty = Column(Integer, nullable=False, default=1)  # 1..3
    content = Column(Text)
    sort_order = Column(Integer, nullable=False, default=0)

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(BigInteger, primary_key=True)
    lesson_id = Column(BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct = Column(String(1), nullable=False)  # A/B/C/D

class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    lesson_id = Column(BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"), primary_key=True)
    status = Column(Text, nullable=False, default="not_started")  # not_started|in_progress|completed
    mastery = Column(Numeric(3,2), nullable=False, default=0.00)
    attempts = Column(Integer, nullable=False, default=0)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    prefer_text = Column(Numeric(3,2), nullable=False, default=0.25)
    prefer_video = Column(Numeric(3,2), nullable=False, default=0.25)
    prefer_interactive = Column(Numeric(3,2), nullable=False, default=0.25)
    prefer_quiz = Column(Numeric(3,2), nullable=False, default=0.25)

class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recommended_lesson_id = Column(BigInteger, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    mode = Column(Text, nullable=False)  # adaptive|baseline
    reason = Column(Text)
    score = Column(Numeric(6,3), nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    accepted = Column(Boolean)

from sqlalchemy import UniqueConstraint

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)

    status = Column(String, nullable=False, default="completed")  # completed | started
    score = Column(Float, nullable=True)  # optional for later quizzes
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_progress_user_lesson"),
    )
