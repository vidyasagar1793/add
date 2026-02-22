from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.models.article import Article
from app.schemas.article import Article as ArticleSchema

router = APIRouter()

@router.get("/", response_model=List[ArticleSchema])
def read_articles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve articles.
    """
    articles = db.query(Article).order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=ArticleSchema)
def read_article(
    *,
    db: Session = Depends(get_db),
    article_id: int,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get article by ID.
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
