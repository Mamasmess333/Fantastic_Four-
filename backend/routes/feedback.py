from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from backend.services.db_service import Feedback, get_session

router = APIRouter(prefix="/feedback", tags=["Feedback"])


class FeedbackPayload(BaseModel):
    user_id: Optional[int] = None
    target_type: str = Field(description="meal_plan, product, analysis")
    target_id: Optional[int] = None
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None


@router.post("")
def submit_feedback(payload: FeedbackPayload):
    with get_session() as session:
        record = Feedback(**payload.dict())
        session.add(record)
        session.flush()
        return {"feedback_id": record.id}


@router.get("")
def list_feedback(target_type: Optional[str] = Query(default=None)):
    with get_session() as session:
        query = session.query(Feedback)
        if target_type:
            query = query.filter(Feedback.target_type == target_type)
        items = query.order_by(Feedback.created_at.desc()).limit(20).all()
        return {
            "count": len(items),
            "feedback": [
                {
                    "id": item.id,
                    "user_id": item.user_id,
                    "target_type": item.target_type,
                    "target_id": item.target_id,
                    "rating": item.rating,
                    "comment": item.comment,
                    "created_at": item.created_at.isoformat(),
                }
                for item in items
            ],
        }

