"""
Tests for authentication endpoints.
"""


def test_register_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert data["data"]["email"] == "test@example.com"
    assert data["data"]["role"] == "user"


def test_register_duplicate_email(client):
    """Test registration fails with duplicate email."""
    payload = {"name": "User", "email": "dup@example.com", "password": "secret123"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


def test_login_success(client):
    """Test successful login returns a token."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "User", "email": "login@example.com", "password": "secret123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Test login fails with wrong password."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "User", "email": "wrong@example.com", "password": "secret123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_get_me_protected(client):
    """Test /auth/me returns the authenticated user."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "Me User", "email": "me@example.com", "password": "secret123"},
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "me@example.com", "password": "secret123"},
    )
    token = login_resp.json()["data"]["access_token"]
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "me@example.com"


def test_get_me_unauthorized(client):
    """Test /auth/me returns 403 without a token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
