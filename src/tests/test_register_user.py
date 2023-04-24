import pytest

from src.tests.conftest import client


register_data = {
        "email": "user@example.com",
        "password": "123456",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    }


def test_user_create_positive():
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 201
    assert response.json()["email"] == register_data["email"]
    assert response.json()["username"] == register_data["username"]
    assert response.json()["role_id"] == register_data["role_id"]


def test_user_create_negative():
    client.post("/auth/register", json=register_data)
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.parametrize("username", ["", "  \n", "     "])
async def test_register_user_validate_username_negative_1(username):
    register_data["username"] = username
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "Username can't be empty"


@pytest.mark.parametrize("username", ["    asd@", "bo$$", "!"])
async def test_register_user_validate_username_negative_2(username):
    register_data["username"] = username
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "Username must be alphanumeric"


@pytest.mark.parametrize("username", ["a" * 51])
async def test_register_user_validate_username_negative_3(username):
    register_data["username"] = username
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "Username must be less than 50 characters"


@pytest.mark.parametrize("username", [["asd"]])
async def test_register_user_validate_username_negative_4(username):
    register_data["username"] = username
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "str type expected"


@pytest.mark.parametrize("password", ["12345", ""])
async def test_register_user_validate_password_negative_1(password):
    register_data["password"] = password
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "Password should beat least 6 characters"


@pytest.mark.parametrize("password", [["asd"]])
async def test_register_user_validate_password_negative_2(password):
    register_data["password"] = password
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "str type expected"


@pytest.mark.parametrize("email", ["ab.com", "@asd.com", "test@test.test", "adda@asda"])
async def test_register_user_validate_email_negative_1(email):
    register_data["email"] = email
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid email address"
