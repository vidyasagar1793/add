import requests
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "password123"

# A reliable RSS feed
RSS_URL = "http://rss.cnn.com/rss/cnn_topstories.rss"

def test_feed_flow():
    # 1. Login to get token
    print("Logging in...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print(f"Login Failed: {response.text}")
            sys.exit(1)
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("Login Successful")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    # 2. Add Feed
    print(f"\nAdding Feed: {RSS_URL}...")
    feed_data = {"name": "CNN Top Stories", "url": RSS_URL}
    response = requests.post(f"{BASE_URL}/feeds/", json=feed_data, headers=headers)
    
    if response.status_code == 200:
        feed_id = response.json()["id"]
        print(f"Feed Added (ID: {feed_id})")
    elif response.status_code == 400 and "already exists" in response.text:
        print("Feed already exists, finding ID...")
        # Get list to find ID
        response = requests.get(f"{BASE_URL}/feeds/", headers=headers)
        feeds = response.json()
        feed = next((f for f in feeds if f["url"] == RSS_URL), None)
        if feed:
            feed_id = feed["id"]
            print(f"Found existing Feed ID: {feed_id}")
        else:
            print("Could not find existing feed ID")
            sys.exit(1)
    else:
        print(f"Add Feed Failed: {response.text}")
        sys.exit(1)

    # 3. Refresh Feed
    print("\nRefreshing Feed...")
    response = requests.post(f"{BASE_URL}/feeds/{feed_id}/refresh", headers=headers)
    if response.status_code == 200:
        new_count = response.json()["new_articles"]
        print(f"Refresh Successful. New Articles: {new_count}")
    else:
        print(f"Refresh Failed: {response.text}")
        sys.exit(1)

    # 4. List Articles
    print("\nListing Articles...")
    response = requests.get(f"{BASE_URL}/articles/", headers=headers)
    if response.status_code == 200:
        articles = response.json()
        print(f"Found {len(articles)} articles.")
        if len(articles) > 0:
            print(f"Top Article: {articles[0]['title']}")
    else:
        print(f"List Articles Failed: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_feed_flow()
