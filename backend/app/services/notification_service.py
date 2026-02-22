from typing import List
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.article import Article
from app.models.user import User

class NotificationService:
    def create_notification(self, db: Session, user_id: int, message: str, article_id: int = None):
        """
        Creates a new notification for a user.
        """
        notification = Notification(
            user_id=user_id,
            message=message,
            article_id=article_id
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    def notify_users_for_new_article(self, db: Session, article: Article):
        """
        Finds users interested in the article's topics and creates notifications.
        """
        if not article.topics:
            return

        # Simple logic: Iterate users and check overlapping topics
        # In a real app, you'd do a complex query join
        users = db.query(User).all()
        for user in users:
            user_topic_ids = {t.id for t in user.topics}
            article_topic_ids = {t.id for t in article.topics}
            
            # Check for intersection
            common_topics = user_topic_ids.intersection(article_topic_ids)
            if common_topics:
                # User is interested!
                # Construct message
                topic_names = [t.name for t in article.topics if t.id in common_topics]
                message = f"New article in {', '.join(topic_names)}: {article.title}"
                
                self.create_notification(db, user.id, message, article.id)

    def get_user_notifications(self, db: Session, user_id: int, skip: int = 0, limit: int = 20):
        return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    def mark_as_read(self, db: Session, notification_id: int, user_id: int):
        notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
        if notification:
            notification.is_read = True
            db.commit()
            return notification
        return None

notification_service = NotificationService()
