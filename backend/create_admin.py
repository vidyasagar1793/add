import os
import sqlite3
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.security import get_password_hash

def log(msg):
    with open("debug.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def create_admin_user():
    # Clear log
    if os.path.exists("debug.txt"):
        os.remove("debug.txt")
        
    db_path = os.path.abspath("sql_app.db")
    db_path = db_path.replace(os.sep, "/")
    log(f"Using DB Path: {db_path}")
    
    # 1. Verify columns with sqlite3
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]
        log(f"Users Table Columns: {columns}")
        
        # Add missing columns
        if "hashed_password" not in columns:
            log("Adding missing column 'hashed_password'...")
            cursor.execute("ALTER TABLE users ADD COLUMN hashed_password VARCHAR")
        
        if "is_active" not in columns:
            log("Adding missing column 'is_active'...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")

        if "is_superuser" not in columns:
            log("Adding missing column 'is_superuser'...")
            cursor.execute("ALTER TABLE users ADD COLUMN is_superuser BOOLEAN DEFAULT 0")
        
        conn.commit()
        conn.close()
    except Exception as e:
        log(f"SQLite3 Schema Fix Error: {e}")

    # 2. Verify with SQLAlchemy
    # Try 3 slashes
    db_url = f"sqlite:///{db_path}"
    log(f"Connection URL: {db_url}")

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        email = "admin@gmail.com"
        password = "admin"
        
        log(f"Querying for user {email}...")
        user = db.query(User).filter(User.email == email).first()
        if user:
            log(f"User {email} already exists.")
            return

        log("Creating new user...")
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        log(f"User {email} created successfully.")
    except Exception as e:
        log(f"ORM Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

