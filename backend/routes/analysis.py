from typing import List, Optional, Tuple

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.ai_service import analyze_image, analyze_text
from backend.services.db_service import save_analysis
from backend.services.nutrition_service import summarize_analysis

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])


class AnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    ingredients: Optional[List[str]] = None
    text_summary: Optional[str] = Field(
        default=None, description="Free-form description of the meal or packaged product."
    )
    user_id: Optional[int] = None
    goal: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None


@router.post("")
async def analyze_existing_image(payload: AnalysisRequest):
    if not payload.image_url and not payload.ingredients and not payload.text_summary:
        raise HTTPException(status_code=400, detail="Provide an image_url or ingredient list.")

    if payload.image_url:
        result = analyze_image(payload.image_url)
    else:
        result = analyze_text(payload.ingredients or [])

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    budget: Optional[Tuple[float, float]] = None
    if payload.budget_min is not None and payload.budget_max is not None:
        budget = (payload.budget_min, payload.budget_max)

    summary = summarize_analysis(
        labels=result["labels"],
        text=payload.text_summary,
        user_goal=payload.goal,
        budget=budget,
    )

    analysis_id = save_analysis(
        user_id=payload.user_id,
        image_url=payload.image_url,
        foods=summary["detected_items"],
        rating=summary["rating"],
        explanation=" ".join(summary["reasons"]),
        alternative=summary["suggestion"],
        metadata={"macros": summary["macros"], "score": summary["score"]},
    )

    return {"analysis_id": analysis_id, **summary}
