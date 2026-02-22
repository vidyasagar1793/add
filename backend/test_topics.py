import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "password123"

def test_topic_flow():
    # 1. Login
    print("Logging in...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            # Try signup if login fails
            print("Login failed, trying signup...")
            signup_data = {"email": EMAIL, "password": PASSWORD}
            requests.post(f"{BASE_URL}/users/", json=signup_data)
            response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
            
        if response.status_code != 200:
             print(f"Auth Failed: {response.text}")
             sys.exit(1)

        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("Login Successful")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # 2. List Topics
    print("\nFetching Topics...")
    response = requests.get(f"{BASE_URL}/topics/", headers=headers)
    if response.status_code == 200:
        topics = response.json()
        print(f"Found {len(topics)} topics.")
        if len(topics) == 0:
            print("No topics found! Seed script might have failed.")
            sys.exit(1)
        first_topic_id = topics[0]["id"]
        print(f"First Topic: {topics[0]['name']} (ID: {first_topic_id})")
    else:
        print(f"Fetch Topics Failed: {response.text}")
        sys.exit(1)

    # 3. Update User Preferences
    print(f"\nSelecting Topic ID {first_topic_id}...")
    update_data = {"topic_ids": [first_topic_id]}
    response = requests.put(f"{BASE_URL}/topics/me", json=update_data, headers=headers)
    if response.status_code == 200:
        user_topics = response.json()
        print(f"User Topics Updated: {len(user_topics)} selected.")
        if user_topics[0]["id"] == first_topic_id:
            print("Verification Successful: Topic correctly assigned.")
        else:
            print("Verification Failed: Assigned topic mismatch.")
    else:
        print(f"Update Preferences Failed: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_topic_flow()
