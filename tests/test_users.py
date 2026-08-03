from app import schemas
from jose import jwt
from app.config import settings
import pytest


# def test_root(client):
#     response = client.get("/")
#     assert response.json().get("message") == "Testing synchronization for development!!!! sort off stuff goes here somehow"
#     assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        "api/v1/users/register",
        json={
            "first_name": "Temitayo",
            "last_name": "Sosanya",
            "email": "tnsosanya@gmail.comii",
            "password": "password@1234"
        })
    assert response.json().get("message") == "User created successfully"
    created_user = schemas.UserResponseEnvelope(**response.json())
    assert created_user.data.email == "tnsosanya@gmail.comii"
    assert response.status_code == 201


def test_user_login(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        })
    assert response.status_code == 200
    login_response = schemas.UserLoginResponse(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert login_response.token_type == "bearer"
    assert id == test_user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("tnsosanya@gmail.comm", "wrongpassword", 403),
    ("tnsosanya@gmail.comaaa", "password@1234", 403),
    (None, "password@1234", 422),
    ("tnsosanya@gmail.comm", None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": password
        })
    assert response.status_code == status_code
    
