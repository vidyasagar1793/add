from fastapi.testclient import TestClient
import pytest

API_V1_STR = "/api/v1"

def test_signup_new_user(client: TestClient):
    email = "test_signup_new@example.com"
    password = "password123"
    signup_data = {"email": email, "password": password}
    response = client.post(f"{API_V1_STR}/users/", json=signup_data)
    assert response.status_code == 200
    assert response.json()["email"] == email

def test_login_success(client: TestClient):
    # Create a user first
    email = "test_login_success@example.com"
    password = "password123"
    client.post(f"{API_V1_STR}/users/", json={"email": email, "password": password})
    
    login_data = {"username": email, "password": password}
    response = client.post(f"{API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None

def test_get_me(client: TestClient, auth_token):
    # uses fixture which provides a valid token
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"{API_V1_STR}/users/me", headers=headers)
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == "test_fixture@example.com"
