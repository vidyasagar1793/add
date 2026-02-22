from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NotificationBase(BaseModel):
    message: str
    is_read: bool = False
    article_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
