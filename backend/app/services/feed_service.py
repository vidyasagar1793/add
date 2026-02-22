from typing import List, Optional
import feedparser
from datetime import datetime
from time import mktime
from sqlalchemy.orm import Session
from app.models.article import Article, Feed
from app.services.ai_service import ai_service

class FeedService:
    async def parse_feed(self, url: str) -> List[dict]:
        """
        Parses an RSS feed asynchronously.
        """
        import httpx
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                content = response.text
            except Exception as e:
                print(f"Error fetching feed {url}: {e}")
                return []

        feed = feedparser.parse(content)
        articles = []
        for entry in feed.entries:
            published_at = None
            if hasattr(entry, 'published_parsed'):
                 published_at = datetime.fromtimestamp(mktime(entry.published_parsed))
            elif hasattr(entry, 'updated_parsed'):
                 published_at = datetime.fromtimestamp(mktime(entry.updated_parsed))

            articles.append({
                "title": entry.title,
                "url": entry.link,
                "summary": getattr(entry, 'summary', None),
                "content": getattr(entry, 'content', [{'value': None}])[0]['value'],
                "published_at": published_at
            })
        return articles

    async def fetch_and_store_articles(self, db: Session, feed_id: int):
        """
        Fetches articles from a specific feed and stores them in the DB.
        """
        feed = db.query(Feed).filter(Feed.id == feed_id).first()
        if not feed:
             return 0

        parsed_articles = await self.parse_feed(feed.url)
        new_count = 0
        
        for article_data in parsed_articles:
            # Check for duplicates
            existing = db.query(Article).filter(Article.url == article_data["url"]).first()
            if not existing:
                db_article = Article(
                    title=article_data["title"],
                    url=article_data["url"],
                    summary=article_data["summary"],
                    content=article_data["content"],
                    published_at=article_data["published_at"],
                    feed_id=feed.id
                )
                db.add(db_article)
                db.commit() # Commit to get ID
                
                # Process with AI Service
                ai_service.process_article(db, db_article)
                
                # Create Notifications
                from app.services.notification_service import notification_service
                notification_service.notify_users_for_new_article(db, db_article)
                
                new_count += 1
        
        feed.last_fetched_at = datetime.utcnow()
        db.commit()
        return new_count

feed_service = FeedService()
