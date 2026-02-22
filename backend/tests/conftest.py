import os
# Force in-memory database for tests
# Use shared cache to ensures multiple connections share the DB
os.environ["DATABASE_URL"] = "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def auth_token(client):
    email = "test_fixture@example.com"
    password = "password123"
    api_v1 = "/api/v1"
    
    # Try signup
    client.post(f"{api_v1}/users/", json={"email": email, "password": password})
    
    # Login
    response = client.post(f"{api_v1}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None
