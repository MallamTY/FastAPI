from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.test_database_name}"
engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def get_db_overrider():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_db_overrider
    yield TestClient(app)



@pytest.fixture(scope="module")
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