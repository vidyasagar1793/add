import requests
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "test@example.com"
PASSWORD = "password123"

def test_ai_pipeline():
    # 1. Login
    print("Logging in...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    # 2. Add a Tech Feed (if not exists) - utilizing TechCrunch for "Technology" topic matching
    RSS_URL = "https://techcrunch.com/feed/"
    print(f"\nAdding/Checking Feed: {RSS_URL}...")
    requests.post(f"{BASE_URL}/feeds/", json={"name": "TechCrunch", "url": RSS_URL}, headers=headers)
    
    # Get Feed ID
    response = requests.get(f"{BASE_URL}/feeds/", headers=headers)
    feeds = response.json()
    feed = next((f for f in feeds if f["url"] == RSS_URL), None)
    if not feed:
        print("Failed to get feed ID")
        sys.exit(1)
    
    # 3. Refresh Feed to trigger AI processing
    print(f"Refreshing Feed (ID: {feed['id']})...")
    response = requests.post(f"{BASE_URL}/feeds/{feed['id']}/refresh", headers=headers)
    print(f"Refresh Response: {response.json()}")

    # 4. Check Articles for Topics and Summary
    print("\nChecking Articles for AI Processing...")
    response = requests.get(f"{BASE_URL}/articles/", headers=headers)
    articles = response.json()
    
    processed_count = 0
    topic_match_count = 0
    
    for article in articles:
        # Check if topics are present (list of topics)
        if article.get("topics") and len(article["topics"]) > 0:
            topic_match_count += 1
            print(f"Article '{article['title'][:30]}...' has topics: {[t['name'] for t in article['topics']]}")
        
        # Check if summary is present and truncated/generated
        if article.get("summary"):
            processed_count += 1
            
    print(f"\nTotal Articles: {len(articles)}")
    print(f"Processed (Summary exists): {processed_count}")
    print(f"Topic Matched: {topic_match_count}")
    
    if processed_count > 0:
        print("AI Pipeline Verification Successful!")
    else:
        print("AI Pipeline Verification Failed: No processing detected.")
        sys.exit(1)

if __name__ == "__main__":
    test_ai_pipeline()
