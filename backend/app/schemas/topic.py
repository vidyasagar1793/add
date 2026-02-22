from typing import List, Optional
from pydantic import BaseModel

class TopicBase(BaseModel):
    name: str
    slug: str

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int

    class Config:
        from_attributes = True

class UserTopicUpdate(BaseModel):
    topic_ids: List[int]
