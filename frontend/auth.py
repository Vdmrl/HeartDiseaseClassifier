import requests

BACKEND_URL = "http://backend:8000"

def login(username: str, password: str) -> str:
    """
    Call the backend /auth/login endpoint.
    Returns the access token if successful.
    """
    payload = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "",
        "client_id": None,
        "client_secret": None,
    }
    response = requests.post(f"{BACKEND_URL}/auth/login", data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        try:
            error_detail = response.json().get("detail", "Login failed")
        except ValueError:
            error_detail = response.text or "Login failed"
        raise Exception(error_detail)

def logout(token: str) -> None:
    """
    Call the backend /auth/logout endpoint.
    """
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(f"{BACKEND_URL}/auth/logout", headers=headers)

def register(email: str, password: str, age: int = None) -> dict:
    """
    Call the backend /auth/register endpoint.
    Returns the registered user data if successful.
    """
    payload = {"email": email, "password": password}
    if age:
        payload["age"] = age
    response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        try:
            error_detail = response.json().get("detail", "Registration failed")
        except ValueError:
            error_detail = response.text or "Registration failed"
        raise Exception(error_detail)

