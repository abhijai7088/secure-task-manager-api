"""
Tests for task CRUD endpoints.
"""


def _get_auth_header(client) -> dict:
    """Register a user, login, and return the auth header."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "Task User", "email": "tasks@example.com", "password": "secret123"},
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "tasks@example.com", "password": "secret123"},
    )
    token = login_resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task(client):
    """Test creating a task."""
    headers = _get_auth_header(client)
    response = client.post(
        "/api/v1/tasks",
        json={"title": "My First Task", "description": "Do something useful"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Task created successfully"
    assert data["data"]["title"] == "My First Task"
    assert data["data"]["status"] == "pending"


def test_list_tasks(client):
    """Test listing tasks returns only the user's tasks."""
    headers = _get_auth_header(client)
    client.post("/api/v1/tasks", json={"title": "Task 1"}, headers=headers)
    client.post("/api/v1/tasks", json={"title": "Task 2"}, headers=headers)
    response = client.get("/api/v1/tasks", headers=headers)
    assert response.status_code == 200
    assert response.json()["total"] == 2


def test_update_task(client):
    """Test updating a task."""
    headers = _get_auth_header(client)
    create_resp = client.post(
        "/api/v1/tasks", json={"title": "Old Title"}, headers=headers
    )
    task_id = create_resp.json()["data"]["id"]
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "New Title", "status": "in_progress"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "New Title"
    assert response.json()["data"]["status"] == "in_progress"


def test_delete_task(client):
    """Test deleting a task."""
    headers = _get_auth_header(client)
    create_resp = client.post(
        "/api/v1/tasks", json={"title": "To Delete"}, headers=headers
    )
    task_id = create_resp.json()["data"]["id"]
    response = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

    # Verify it's gone
    get_resp = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_resp.status_code == 404
