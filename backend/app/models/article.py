from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base
from app.models.associations import article_topics # Explicit import

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    last_fetched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Article", back_populates="feed")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=True)  # Full content or summary
    summary = Column(Text, nullable=True) # AI generated summary later
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    feed = relationship("Feed", back_populates="articles")
    
    is_processed = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    # Import association table here to avoid circular import at module level if possible, 
    # but for secondary, string is usually fine if metadata has it. 
    # To be safe, let's use the table name string but ensure associations is imported in main.
    # Actually, importing the object is safer.
    
    topics = relationship("Topic", secondary="article_topics", back_populates="articles")

