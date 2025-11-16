from fastapi.testclient import TestClient
from fastapi import status


def test_register_successfully(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "due_date": "2026-05-10"
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_register_conflict(client: TestClient):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "due_date": "2026-05-10"
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123",
            "due_date": "2026-05-10"
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Username or email already in use"