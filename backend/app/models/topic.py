from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.associations import article_topics # Explicit import

# Many-to-Many relationship table
user_topics = Table(
    "user_topics",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    # Relationship to users
    users = relationship("User", secondary=user_topics, backref="topics")
    
    # Relationship to articles
    articles = relationship("Article", secondary="article_topics", back_populates="topics")

