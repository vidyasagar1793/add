from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models import Topic, User, Notification # Import models to ensure they are registered

def init_db(db: Session):
    topics = [
        {"name": "Technology", "slug": "technology"},
        {"name": "Artificial Intelligence", "slug": "artificial-intelligence"},
        {"name": "Programming", "slug": "programming"},
        {"name": "Startups", "slug": "startups"},
        {"name": "Science", "slug": "science"},
        {"name": "Health", "slug": "health"},
        {"name": "Politics", "slug": "politics"},
        {"name": "Business", "slug": "business"},
        {"name": "Entertainment", "slug": "entertainment"},
        {"name": "Sports", "slug": "sports"},
        {"name": "Cryptocurrency", "slug": "cryptocurrency"},
        {"name": "Cybersecurity", "slug": "cybersecurity"},
    ]

    for topic_data in topics:
        topic = db.query(Topic).filter(Topic.slug == topic_data["slug"]).first()
        if not topic:
            topic = Topic(name=topic_data["name"], slug=topic_data["slug"])
            db.add(topic)
            print(f"Added topic: {topic_data['name']}")
        else:
            print(f"Topic exists: {topic_data['name']}")
    
    db.commit()

if __name__ == "__main__":
    from app.db.session import Base, engine
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialized with topics.")
    finally:
        db.close()
