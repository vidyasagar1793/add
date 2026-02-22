from typing import List, Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.models.article import Feed
from app.schemas.article import Feed as FeedSchema, FeedCreate
from app.services.feed_service import FeedService

router = APIRouter()
feed_service = FeedService()

@router.post("/", response_model=FeedSchema)
def create_feed(
    *,
    db: Session = Depends(get_db),
    feed_in: FeedCreate,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new feed.
    """
    feed = db.query(Feed).filter(Feed.url == str(feed_in.url)).first()
    if feed:
        raise HTTPException(
            status_code=400,
            detail="The feed with this URL already exists in the system.",
        )
    feed = Feed(name=feed_in.name, url=str(feed_in.url))
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed

@router.get("/", response_model=List[FeedSchema])
def read_feeds(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve feeds.
    """
    feeds = db.query(Feed).offset(skip).limit(limit).all()
    return feeds

@router.post("/{feed_id}/refresh", response_model=Dict[str, int])
async def refresh_feed(
    feed_id: int,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Manually trigger a refresh for a specific feed.
    """
    count = await feed_service.fetch_and_store_articles(db, feed_id=feed_id)
    return {"new_articles": count}
