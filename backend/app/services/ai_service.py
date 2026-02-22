from typing import List
from sqlalchemy.orm import Session
from app.models.topic import Topic
from app.models.article import Article

class AIService:
    def classify_article(self, db: Session, content: str, title: str) -> List[Topic]:
        """
        Heuristic classification based on keyword matching.
        """
        all_topics = db.query(Topic).all()
        matched_topics = []
        
        text_to_scan = (title + " " + content).lower()
        
        for topic in all_topics:
            # Simple keyword matching: check if topic name or slug is in text
            if topic.name.lower() in text_to_scan or topic.slug.replace("-", " ") in text_to_scan:
                matched_topics.append(topic)
                
        return matched_topics

    def summarize_article(self, content: str) -> str:
        """
        Simple truncation for MVP summary.
        """
        if not content:
            return ""
        
        # Strip HTML tags if any (very basic)
        import re
        clean_text = re.sub('<[^<]+?>', '', content)
        
        if len(clean_text) <= 200:
            return clean_text
        
        return clean_text[:197] + "..."

    def process_article(self, db: Session, article: Article):
        """
        Run classification and summarization on an article.
        """
        if article.is_processed:
            return

        # Generate Summary
        if not article.summary:
            article.summary = self.summarize_article(article.content or "")

        # Classify
        topics = self.classify_article(db, article.content or "", article.title)
        article.topics = topics
        
        article.is_processed = True
        db.add(article)
        db.commit()

ai_service = AIService()
