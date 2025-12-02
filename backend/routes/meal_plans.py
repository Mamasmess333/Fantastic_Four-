from typing import List, Optional, Tuple

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.db_service import MealPlan, get_session
from backend.services.meal_plan_service import generate_meal_plan

router = APIRouter(prefix="/meal-plans", tags=["Meal Plans"])


class MealPlanRequest(BaseModel):
    user_id: Optional[int] = None
    goal: str = Field(default="health", description="fitness, health, budget")
    budget_min: float = 5
    budget_max: float = 15
    preferences: List[str] = []
    allergies: List[str] = []
    days: int = Field(default=3, ge=1, le=7)


@router.post("/generate")
def create_meal_plan(payload: MealPlanRequest):
    budget: Tuple[float, float] = (payload.budget_min, payload.budget_max)
    plan = generate_meal_plan(
        goal=payload.goal,
        budget=budget,
        preferences=payload.preferences,
        allergies=payload.allergies,
        days=payload.days,
    )
    with get_session() as session:
        record = MealPlan(user_id=payload.user_id, goal=payload.goal, budget=payload.budget_max, plan=plan)
        session.add(record)
        session.flush()
        return {"plan_id": record.id, **plan}


@router.get("/{plan_id}")
def get_meal_plan(plan_id: int):
    with get_session() as session:
        plan = session.get(MealPlan, plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Meal plan not found.")
        return {"plan_id": plan.id, **plan.plan}

