import pytest

from snippets.api.routes.v1.user import router as user_router
from snippets.crud.user import create_user, get_user
from snippets.models.user import UserCreate
from tests.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestUserRouter(BaseTestRouter):
    router = user_router

    async def test_create_user(self, client):
        data = {"email": "test@example.com", "password": "password"}
        response = await client.post("/users/", json=data)
        assert response.status_code == 201
        assert response.json()["email"] == data["email"]

    async def test_get_user(self, session, client):
        user = await create_user(session, UserCreate(email="test@example.com"))
        response = await client.get(f"/users/{user.id}")
        assert response.status_code == 200
        assert response.json()["email"] == user.email

    async def test_update_user(self, session, client):
        user = await create_user(session, UserCreate(email="test@example.com"))
        response = await client.patch(
            f"/users/{user.id}", json=dict(email="test1@example.com")
        )
        assert response.status_code == 200
        assert response.json()["email"] == user.email

        user_updated = await get_user(session, id=user.id)
        assert user_updated.email == "test1@example.com"

    async def test_delete_user(self, session, client):
        user = await create_user(session, UserCreate(email="test@example.com"))
        response = await client.delete(f"/users/{user.id}")
        assert response.status_code == 200
        assert response.json() == dict(deleted=1)

        user_deleted = await get_user(session, id=user.id)
        assert user_deleted is None
