import httpx
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_register_success(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "due_date": "2026-05-10",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_register_conflict(client: httpx.AsyncClient) -> None:
    await client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "due_date": "2026-05-10",
        },
    )

    response = await client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "password123",
            "due_date": "2026-05-10",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Username or email already in use"
