from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.services.notification_service import notification_service
from app.schemas.notification import Notification

router = APIRouter()

@router.get("/", response_model=List[Notification])
def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve current user's notifications.
    """
    return notification_service.get_user_notifications(db, user_id=current_user.id, skip=skip, limit=limit)

@router.put("/{notification_id}/read", response_model=Notification)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a notification as read.
    """
    notification = notification_service.mark_as_read(db, notification_id=notification_id, user_id=current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
