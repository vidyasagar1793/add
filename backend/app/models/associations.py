from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

article_topics = Table(
    "article_topics",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topics.id"), primary_key=True),
)
