from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from backend.services.notification_service import list_notifications, schedule_notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationPayload(BaseModel):
    user_id: Optional[int] = None
    message: str
    category: str = "reminder"
    send_in_minutes: int = 60
    metadata: dict = Field(default_factory=dict)


@router.post("")
def create_notification(payload: NotificationPayload):
    notification_id = schedule_notification(
        user_id=payload.user_id,
        message=payload.message,
        category=payload.category,
        send_in_minutes=payload.send_in_minutes,
        metadata=payload.metadata,
    )
    return {"notification_id": notification_id}


@router.get("")
def list_user_notifications(user_id: Optional[int] = Query(default=None)):
    notifications = list_notifications(user_id=user_id)
    return {"count": len(notifications), "notifications": notifications}

