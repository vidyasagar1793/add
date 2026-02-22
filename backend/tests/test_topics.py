from fastapi.testclient import TestClient

API_V1_STR = "/api/v1"

def test_list_topics(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = client.get(f"{API_V1_STR}/topics/", headers=headers)
    assert response.status_code == 200
    topics = response.json()
    assert isinstance(topics, list)

def test_update_user_topics(client: TestClient, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Get topics first
    response = client.get(f"{API_V1_STR}/topics/", headers=headers)
    assert response.status_code == 200
    topics = response.json()
    
    if not topics:
        print("No topics found, skipping update test")
        return

    first_topic_id = topics[0]["id"]
    
    update_data = {"topic_ids": [first_topic_id]}
    response = client.put(f"{API_V1_STR}/topics/me", json=update_data, headers=headers)
    
    assert response.status_code == 200
    user_topics = response.json()
    assert len(user_topics) > 0
    assert user_topics[0]["id"] == first_topic_id
