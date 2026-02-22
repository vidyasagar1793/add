import requests

def test_login():
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "username": "admin@gmail.com",
        "password": "admin"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Login Successful!")
            print("Response:", response.json())
        else:
            print("Login Failed!")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
