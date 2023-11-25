import httpx
import pytest

from app import app
from app_scope import app as app_scope


@pytest.mark.asyncio
async def test_login():
    async with httpx.AsyncClient(app=app_scope, base_url="http://localhost:8000") as ac:
        response = await ac.post("/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200
    print(response.json())
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None


@pytest.mark.asyncio
async def test_get_user_me():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/me", headers={"Authorization": "Bearer johndoe"})
    assert response.status_code == 200
    assert response.text is not None
    print("response.json()")
    print(response.json())


@pytest.mark.asyncio
async def test_get_item():
    async with httpx.AsyncClient(app=app_scope, base_url="http://test") as ac:
        response = await ac.post("/token",
                                 data={"username": "johndoe", "password": "secret", "scope": "items me"})
        token = response.json()["access_token"]
        response = await ac.get("/users/me/items/", headers={"Authorization": f"Bearer {token}"})
    print("response.json()")
    print(response.json())
    assert response.status_code == 200
    assert response.text is not None
