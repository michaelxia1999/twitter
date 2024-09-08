import pytest
import pytest_asyncio
from app.main import app as _app
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def app():
    async with LifespanManager(app=_app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        await client.aclose()


@pytest.mark.asyncio(loop_scope="module")
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={"username": "username", "password": "password", "email": "email"})
    assert response.status_code == 201
    assert response.json()["username"] == "username"
    assert response.json()["password"] == "password"
    assert response.json()["email"] == "email"
    assert "id" in response.json()
    assert "created_at" in response.json()
