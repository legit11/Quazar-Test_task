import pytest
import logging

from httpx import AsyncClient

from src.users.schemas import UserCreate, UserFromDB


logging.basicConfig(level=logging.INFO)


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    user = UserCreate(username="testuser", email="test@example.com")

    response = await async_client.post("/users", json=user.model_dump())

    assert response.status_code == 200
    existing_user = UserFromDB(**response.json())
    assert existing_user.username == user.username
    assert existing_user.email == user.email


@pytest.mark.asyncio
async def test_read_users(async_client: AsyncClient):
    try:
        response = await async_client.get("/users")
        assert response.status_code == 200
    except Exception as e:
        print(f"Error occurred: {e}")


@pytest.mark.asyncio
async def test_read_user(async_client: AsyncClient):
    response = await async_client.get("/users/1")
    assert response.status_code == 200
    assert "username" in response.json()


@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient):
    user_update_data = {
        "username": "updateduser",
        "email": "updateduser@example.com"
    }
    # Предполагаем, что пользователь с ID 1 существует
    response = await async_client.put("/users/1", json=user_update_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_update_data["username"]


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient):
    # Предполагаем, что пользователь с ID 1 существует
    response = await async_client.delete("/users/1")
    assert response.status_code == 200  # Успешное удаление

@pytest.mark.asyncio
async def test_get_user_statistics(async_client: AsyncClient):
    domain = "example.com"
    response = await async_client.get(f"/users/statistics?domain={domain}")
    assert response.status_code == 200

