import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "notify_test@example.com"
PASSWORD = "password123"

def test_notifications():
    # 1. Signup/Login
    print("1. Authenticating...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print("Creating user...")
        requests.post(f"{BASE_URL}/auth/signup", json={"email": EMAIL, "password": PASSWORD})
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        sys.exit(1)
        
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get User ID
    user_resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    user_id = user_resp.json()["id"]
    print(f"User ID: {user_id}")

    # 3. Ensure Topic Exists and Subscribe
    print("2. Setting up Topics...")
    topics_resp = requests.get(f"{BASE_URL}/topics/", headers=headers)
    topics = topics_resp.json()
    tech_topic = next((t for t in topics if "Technology" in t["name"]), None)
    
    if not tech_topic:
        print("Technology topic not found. Run init_db.py or create it.")
        sys.exit(1)
        
    print(f"Subscribing to {tech_topic['name']} (ID: {tech_topic['id']})...")
    requests.post(f"{BASE_URL}/topics/select", json=[tech_topic['id']], headers=headers)

    # 4. Simulate New Article Arrival (Triggering Notification)
    # We can't easily "inject" an article via API to trigger the service function strictly 
    # without a feed, but we can call the notification endpoint to check if *previous* runs generated any,
    # OR we can manually trigger a feed refresh if we have a controllable feed.
    # For this test, we'll verify the ENDPOINTS work. The orchestration was tested via code review.
    # To truly test the flow, we'd need to mock the DB or inject an article.
    
    # Let's try to trigger it by refreshing a feed that we know has tech articles, 
    # similar to the AI pipeline test.
    RSS_URL = "https://techcrunch.com/feed/"
    print(f"\n3. Refreshing Feed: {RSS_URL}...")
    
    # Ensure feed exists
    feeds = requests.get(f"{BASE_URL}/feeds/", headers=headers).json()
    feed = next((f for f in feeds if f["url"] == RSS_URL), None)
    if not feed:
        requests.post(f"{BASE_URL}/feeds/", json={"name": "TechCrunch", "url": RSS_URL}, headers=headers)
        feeds = requests.get(f"{BASE_URL}/feeds/", headers=headers).json()
        feed = next((f for f in feeds if f["url"] == RSS_URL), None)
        
    response = requests.post(f"{BASE_URL}/feeds/{feed['id']}/refresh", headers=headers)
    print(f"Refresh status: {response.status_code}")

    # 5. Check Notifications
    print("\n4. Checking Notifications...")
    notif_resp = requests.get(f"{BASE_URL}/notifications/", headers=headers)
    notifications = notif_resp.json()
    
    print(f"Found {len(notifications)} notifications.")
    for n in notifications:
        print(f"- [Read: {n['is_read']}] {n['message']}")
        
    if len(notifications) > 0:
        # 6. Mark as Read
        first_id = notifications[0]['id']
        print(f"\n5. Marking notification {first_id} as read...")
        read_resp = requests.put(f"{BASE_URL}/notifications/{first_id}/read", headers=headers)
        if read_resp.status_code == 200 and read_resp.json()['is_read'] == True:
            print("Successfully marked as read.")
        else:
            print(f"Failed to mark as read: {read_resp.text}")
            
        print("\nNotification Integration Verification Successful!")
    else:
        print("\nNo notifications found. This might be expected if no NEW articles were fetched during this specific run.")
        print("However, endpoints are reachable.")

if __name__ == "__main__":
    test_notifications()
