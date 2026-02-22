import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "analytics_test@example.com"
PASSWORD = "password123"

def test_analytics():
    # 1. Login/Signup
    print("1. Authenticating...")
    login_data = {"username": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print("Creating user...")
        resp = requests.post(f"{BASE_URL}/auth/signup", json={"email": EMAIL, "password": PASSWORD})
        if resp.status_code != 200:
             print(f"Signup failed: {resp.text}")
             sys.exit(1)
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        sys.exit(1)
        
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get an Article
    print("\n2. Fetching Articles...")
    articles_resp = requests.get(f"{BASE_URL}/articles/", headers=headers)
    articles = articles_resp.json()
    
    if not articles:
        print("No articles found. Adding a feed first...")
        # Add feed if needed
        requests.post(f"{BASE_URL}/feeds/", json={"name": "TechCrunch", "url": "https://techcrunch.com/feed/"}, headers=headers)
        # Refresh
        # We need feed ID
        feeds = requests.get(f"{BASE_URL}/feeds/", headers=headers).json()
        if feeds:
            requests.post(f"{BASE_URL}/feeds/{feeds[0]['id']}/refresh", headers=headers)
            articles = requests.get(f"{BASE_URL}/articles/", headers=headers).json()
    
    if not articles:
        print("Still no articles. Exiting.")
        sys.exit(1)
        
    article = articles[0]
    initial_views = article.get("view_count", 0)
    print(f"Article '{article['title'][:30]}...' has {initial_views} views.")

    # 3. Increment View Count
    print(f"\n3. Incrementing view count for Article ID {article['id']}...")
    view_resp = requests.post(f"{BASE_URL}/analytics/article/{article['id']}/view", headers=headers)
    
    if view_resp.status_code != 200:
        print(f"Failed to increment view: {view_resp.text}")
        sys.exit(1)
        
    updated_article = view_resp.json()
    new_views = updated_article["view_count"]
    print(f"New view count: {new_views}")
    
    if new_views == initial_views + 1:
        print("SUCCESS: View count incremented correctly.")
    else:
        print("FAILURE: View count did not increment as expected.")

if __name__ == "__main__":
    test_analytics()
