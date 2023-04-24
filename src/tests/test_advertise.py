from httpx import AsyncClient

from src.tests.test_register_user import register_data

json_data = {
    "id": 5,
    "name": "string",
    "address": "string",
    "price": 100,
    "created_at": "2023-04-21T15:27:49.129",
    "description": "string",
    "image_url": "string"
}


async def test_add_advertise(async_client: AsyncClient):
    response = await async_client.post("/auth/register", json=register_data)
    assert response.status_code == 201

    response = await async_client.post(
        "auth/jwt/login",
        data={
            "username": "user@example.com",
            "password": "123456"
        }
    )
    assert response.status_code == 200

    response = await async_client.post("/advertise", json=json_data)
    assert response.status_code == 200
