from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from backend.services.db_service import MealAnalysis, MealPlan, User, get_session

router = APIRouter(prefix="/users", tags=["Users"])


class UserPayload(BaseModel):
    name: str
    email: EmailStr
    dietary_preferences: List[str] = []
    allergies: List[str] = []
    goal: str = "health"
    budget_min: float = 0
    budget_max: float = 120
    language: str = "en"


class UserUpdate(BaseModel):
    dietary_preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    goal: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    language: Optional[str] = None


def _serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "dietary_preferences": user.dietary_preferences,
        "allergies": user.allergies,
        "goal": user.goal,
        "budget": {"min": user.budget_min, "max": user.budget_max},
        "language": user.language,
        "created_at": user.created_at.isoformat(),
    }


@router.post("")
def create_user(payload: UserPayload):
    with get_session() as session:
        if session.query(User).filter(User.email == payload.email).first():
            raise HTTPException(status_code=409, detail="Email already registered.")
        user = User(**payload.dict())
        session.add(user)
        session.flush()
        return _serialize_user(user)


@router.get("/{user_id}")
def get_user(user_id: int):
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return _serialize_user(user)


@router.patch("/{user_id}")
def update_user(user_id: int, payload: UserUpdate):
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        for field, value in payload.dict(exclude_unset=True).items():
            setattr(user, field, value)
        session.add(user)
        session.flush()
        return _serialize_user(user)


@router.get("/{user_id}/history")
def user_history(user_id: int):
    with get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        analyses = (
            session.query(MealAnalysis)
            .filter(MealAnalysis.user_id == user_id)
            .order_by(MealAnalysis.created_at.desc())
            .limit(10)
            .all()
        )
        plans = (
            session.query(MealPlan)
            .filter(MealPlan.user_id == user_id)
            .order_by(MealPlan.created_at.desc())
            .limit(5)
            .all()
        )
        return {
            "user": _serialize_user(user),
            "analyses": [
                {
                    "id": analysis.id,
                    "rating": analysis.rating,
                    "detected_items": analysis.detected_items,
                    "alternative": analysis.alternative,
                    "created_at": analysis.created_at.isoformat(),
                }
                for analysis in analyses
            ],
            "meal_plans": [
                {"id": plan.id, "goal": plan.goal, "created_at": plan.created_at.isoformat(), "budget": plan.plan.get("budget")}
                for plan in plans
            ],
        }

