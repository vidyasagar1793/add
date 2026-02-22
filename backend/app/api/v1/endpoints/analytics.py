from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.article import Article
from app.schemas.article import Article as ArticleSchema

router = APIRouter()

@router.post("/article/{article_id}/view", response_model=ArticleSchema)
def increment_view_count(
    article_id: int,
    db: Session = Depends(deps.get_db),
    # Optional: require auth, or allow anonymous views? 
    # For now, let's allow anyone or require at least a token if we sort by views personalized.
    # Let's keep it open or just Require user to be logged in to be safe.
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Increment the view count for an article.
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.view_count += 1
    db.commit()
    db.refresh(article)
    return article
