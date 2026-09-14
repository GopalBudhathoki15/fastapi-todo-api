def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )

    assert response.status_code == 201


def test_register_user_with_duplicate_email(client):
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )
    response = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )

    assert response.status_code == 409


def test_login_user(client):
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "12345678"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_login_with_wrong_password(client):
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "1234567810"},
    )

    assert response.status_code == 401


def test_login_with_wrong_email(client):
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "12345678"},
    )

    assert response.status_code == 401
