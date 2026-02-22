import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "password123"

def test_auth_flow():
    # 1. Signup
    print("Testing Signup...")
    signup_data = {"email": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(f"{BASE_URL}/users/", json=signup_data)
        if response.status_code == 200:
            print("Signup Successful")
        elif response.status_code == 400 and "already exists" in response.text:
            print("User already exists, proceeding...")
        else:
            print(f"Signup Failed: {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # 2. Login
    print("\nTesting Login...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Login Successful, Token received")
    else:
        print(f"Login Failed: {response.text}")
        sys.exit(1)

    # 3. Get Me
    print("\nTesting Get Me...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    if response.status_code == 200:
        user = response.json()
        if user["email"] == EMAIL:
             print(f"Get Me Successful: {user['email']}")
        else:
             print("Get Me Failed: Email mismatch")
    else:
        print(f"Get Me Failed: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_auth_flow()
