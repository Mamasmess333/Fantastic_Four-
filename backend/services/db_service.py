import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/bitewise.db")

if DATABASE_URL.startswith("sqlite"):
    Path("data").mkdir(exist_ok=True)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    dietary_preferences = Column(JSON, default=list)
    allergies = Column(JSON, default=list)
    goal = Column(String, default="health")
    budget_min = Column(Float, default=0.0)
    budget_max = Column(Float, default=100.0)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("MealAnalysis", back_populates="user", cascade="all, delete-orphan")
    plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class MealAnalysis(Base):
    __tablename__ = "meal_analyses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_url = Column(String, nullable=True)
    detected_items = Column(JSON, default=list)
    rating = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    alternative = Column(String, nullable=False)
    meta = Column("metadata", JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    goal = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    plan = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plans")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    message = Column(String, nullable=False)
    category = Column(String, default="reminder")
    send_at = Column(DateTime, default=datetime.utcnow)
    sent = Column(Boolean, default=False)
    meta = Column("metadata", JSON, default=dict)

    user = relationship("User", back_populates="notifications")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    """Ensure local SQLite directory exists and create tables."""
    if DATABASE_URL.startswith("sqlite"):
        Path("data").mkdir(exist_ok=True)
    Base.metadata.create_all(bind=engine)


# Ensure tables exist for tests and local scripts without FastAPI startup.
init_db()


@contextmanager
def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def save_analysis(
    *,
    user_id: Optional[int],
    image_url: Optional[str],
    foods,
    rating: str,
    explanation: str,
    alternative: str,
    metadata: Optional[dict] = None,
):
    with get_session() as session:
        analysis = MealAnalysis(
            user_id=user_id,
            image_url=image_url,
            detected_items=foods,
            rating=rating,
            explanation=explanation,
            alternative=alternative,
            meta=metadata or {},
        )
        session.add(analysis)
        session.flush()
        return analysis.id
   