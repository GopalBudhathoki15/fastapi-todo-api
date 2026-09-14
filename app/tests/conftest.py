from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.main import app
from fastapi.testclient import TestClient
from app.database import get_db
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("TEST_DATABASE_URL")

if database_url is None:
    raise RuntimeError("TEST_DATABASE_URL is not set")

test_engine = create_engine(database_url)


@pytest.fixture
def client():
    connection = test_engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    try:
        yield client

    finally:
        app.dependency_overrides.clear()
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def auth_headers(client):
    client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "12345678"},
    )

    login_response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "12345678"}
    )

    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
