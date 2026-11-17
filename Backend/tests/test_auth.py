def test_login_admin_success(client):
    """Test login with admin credentials returns token and user info."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["username"] == "admin"
    assert data["user"]["role"] == "admin"


def test_login_operator_success(client):
    """Test login with operator credentials returns token and user info."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "operator", "password": "operator123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user"]["username"] == "operator"
    assert data["user"]["role"] == "user"


def test_login_invalid_password(client):
    """Test login with wrong password returns 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with nonexistent user returns 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent_user_99", "password": "password"}
    )
    assert response.status_code == 401


def test_logout(client):
    """Test logout endpoint returns success."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_users(client):
    """Test retrieving user management list."""
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 2
    usernames = [u["username"] for u in users]
    assert "admin" in usernames
    assert "operator" in usernames


def test_create_and_delete_user(client):
    """Test creating a new user and deleting them."""
    new_user_data = {
        "name": "Jane Logistics",
        "username": "jane.logistics",
        "email": "jane@twinflow.ai",
        "password": "securepass123",
        "role": "user",
        "status": "Active",
        "accessLevel": "Floor Operator"
    }
    # Create
    create_res = client.post("/api/v1/users", json=new_user_data)
    assert create_res.status_code == 200
    assert create_res.json()["success"] is True

    # Duplicate username check
    dup_res = client.post("/api/v1/users", json=new_user_data)
    assert dup_res.status_code == 400

    # Verify user is listed
    list_res = client.get("/api/v1/users")
    created_user = next((u for u in list_res.json() if u["username"] == "jane.logistics"), None)
    assert created_user is not None
    user_id = created_user["id"]

    # Update user
    update_res = client.put(f"/api/v1/users/{user_id}", json={"name": "Jane Supervisor", "status": "Inactive"})
    assert update_res.status_code == 200

    # Delete user
    del_res = client.delete(f"/api/v1/users/{user_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Verify deletion
    verify_list = client.get("/api/v1/users")
    deleted_user = next((u for u in verify_list.json() if u["username"] == "jane.logistics"), None)
    assert deleted_user is None
