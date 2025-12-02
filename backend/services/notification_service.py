from datetime import datetime, timedelta
from typing import List, Optional

from backend.services.db_service import Notification, get_session


def schedule_notification(
    *,
    user_id: Optional[int],
    message: str,
    category: str = "reminder",
    send_in_minutes: int = 60,
    metadata: Optional[dict] = None,
) -> int:
    send_at = datetime.utcnow() + timedelta(minutes=send_in_minutes)
    with get_session() as session:
        note = Notification(
            user_id=user_id,
            message=message,
            category=category,
            send_at=send_at,
            meta=metadata or {},
        )
        session.add(note)
        session.flush()
        return note.id


def list_notifications(user_id: Optional[int] = None) -> List[dict]:
    with get_session() as session:
        query = session.query(Notification)
        if user_id:
            query = query.filter(Notification.user_id == user_id)
        rows = query.order_by(Notification.send_at.desc()).all()
        serialized = []
        for note in rows:
            serialized.append(
                {
                    "id": note.id,
                    "user_id": note.user_id,
                    "message": note.message,
                    "category": note.category,
                    "send_at": note.send_at.isoformat(),
                    "sent": note.sent,
                    "metadata": note.meta,
                }
            )
        return serialized

