def test_get_tasks(client, auth_headers):

    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200


def test_create_task(client, auth_headers):

    response = client.post(
        "/tasks", json={"title": "Learn Fastapi fast"}, headers=auth_headers
    )

    assert response.status_code == 201


def test_get_a_task_by_id(client, auth_headers):

    create_response = client.post(
        "/tasks", json={"title": "Learn Backend fast"}, headers=auth_headers
    )

    task_id = create_response.json()["id"]

    get_respone = client.get(f"/tasks/{task_id}", headers=auth_headers)

    assert get_respone.status_code == 200


def test_delete_a_task(client, auth_headers):

    create_response = client.post(
        "/tasks", json={"title": "Learn Backend fast"}, headers=auth_headers
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)

    assert delete_response.status_code == 204


def test_update_a_task(client, auth_headers):
    create_response = client.post(
        "/tasks", json={"title": "Learn Backend fast"}, headers=auth_headers
    )

    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}", json={"title": "Learn Backend Fast"}, headers=auth_headers
    )

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Learn Backend Fast"


def test_user_should_be_unable_to_access_others_tasks(client, auth_headers):
    client.post(
        "/auth/register",
        json={
            "name": "Another User",
            "email": "anotheruser@example.com",
            "password": "12345678",
        },
    )

    login_response = client.post(
        "/auth/login", json={"email": "anotheruser@example.com", "password": "12345678"}
    )

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    create_response = client.post(
        "/tasks", json={"title": "Learn Python"}, headers=auth_headers
    )

    response = client.get(f"/tasks/{create_response.json()["id"]}", headers=headers)

    assert response.status_code == 404
