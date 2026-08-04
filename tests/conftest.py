from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.test_database_name}"
engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def get_db_overrider():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_db_overrider
    yield TestClient(app)



@pytest.fixture()
def test_user(client):
    user_data = {
            "first_name": "Temitayo",
            "last_name": "Sosanya",
            "email": "tnsosanya@gmail.comm",
            "password": "password@1234"
        }
    response = client.post(
        "api/v1/users/register",
        json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user = new_user.get("data")
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "First Post",
            "content": "Content of first post",
            "poster_id": test_user["id"]
        },
        {
            "title": "Second Post",
            "content": "Content of second post",
            "poster_id": test_user["id"]
        },
        {
            "title": "Third Post",
            "content": "Content of third post",
            "poster_id": test_user["id"]
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
     
