from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, feeds, articles, topics, notifications, analytics

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(feeds.router, prefix="/feeds", tags=["feeds"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

