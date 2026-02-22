from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.models.topic import Topic
from app.models.user import User
from app.schemas.topic import Topic as TopicSchema, TopicCreate, UserTopicUpdate

router = APIRouter()

@router.get("/", response_model=List[TopicSchema])
def read_topics(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all available topics.
    """
    topics = db.query(Topic).offset(skip).limit(limit).all()
    return topics

@router.post("/", response_model=TopicSchema)
def create_topic(
    *,
    db: Session = Depends(get_db),
    topic_in: TopicCreate,
    current_user: User = Depends(deps.get_current_user), # Admin only in real app
) -> Any:
    """
    Create a new topic.
    """
    topic = db.query(Topic).filter(Topic.slug == topic_in.slug).first()
    if topic:
        raise HTTPException(
            status_code=400,
            detail="The topic with this slug already exists.",
        )
    topic = Topic(name=topic_in.name, slug=topic_in.slug)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

@router.get("/me", response_model=List[TopicSchema])
def read_user_topics(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve current user's selected topics.
    """
    return current_user.topics

@router.put("/me", response_model=List[TopicSchema])
def update_user_topics(
    *,
    db: Session = Depends(get_db),
    topic_update: UserTopicUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update current user's selected topics. Replace existing selection.
    """
    # Verify topics exist
    topics = db.query(Topic).filter(Topic.id.in_(topic_update.topic_ids)).all()
    if len(topics) != len(topic_update.topic_ids):
         raise HTTPException(status_code=400, detail="One or more topic IDs are invalid")

    current_user.topics = topics
    db.commit()
    db.refresh(current_user)
    return current_user.topics
