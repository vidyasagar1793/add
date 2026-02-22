from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl

# --- Article Schemas ---
class ArticleBase(BaseModel):
    title: str
    url: HttpUrl
    summary: Optional[str] = None
    published_at: Optional[datetime] = None

class ArticleCreate(ArticleBase):
    content: Optional[str] = None
    feed_id: int

from app.schemas.topic import Topic

class Article(ArticleBase):
    id: int
    feed_id: int
    created_at: datetime
    view_count: int = 0
    topics: List[Topic] = []

    class Config:
        from_attributes = True

# --- Feed Schemas ---
class FeedBase(BaseModel):
    name: str
    url: HttpUrl

class FeedCreate(FeedBase):
    pass

class Feed(FeedBase):
    id: int
    is_active: bool
    last_fetched_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
