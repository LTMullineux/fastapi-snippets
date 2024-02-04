import pytest
from snippets.crud import IntegrityConflictException, UserCrud
from snippets.models import UserInSchema, UserUpdateSchema


@pytest.mark.asyncio
class TestUserCrud:
    async def test_create_user(self, session):
        user_create = UserInSchema(
            username="test",
            email="test@test.com",
            password="password",
        )
        user = await UserCrud.create(session, user_create)
        assert user.uuid is not None
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.username == "test"
        assert user.email == "test@test.com"
        assert user.is_active is True
        assert user.hashed_password == "drowssap"

    async def test_create_user_conflict_username(self, session):
        user_create = UserInSchema(
            username="test",
            email="test@test.com",
            password="password",
        )
        _ = await UserCrud.create(session, user_create)

        user_conflict = UserInSchema(
            username="test",
            email="test1@test.com",
            password="password",
        )
        with pytest.raises(IntegrityConflictException):
            _ = await UserCrud.create(session, user_conflict)

    async def test_create_user_conflict_email(self, session):
        user_create = UserInSchema(
            username="test",
            email="test@test.com",
            password="password",
        )
        _ = await UserCrud.create(session, user_create)

        user_conflict = UserInSchema(
            username="test1",
            email="test@test.com",
            password="password",
        )
        with pytest.raises(IntegrityConflictException):
            _ = await UserCrud.create(session, user_conflict)

    async def test_update_user(self, session):
        user_create = UserInSchema(
            username="test",
            email="test@test.com",
            password="password",
        )
        user = await UserCrud.create(session, user_create)

        user_update = await UserCrud.update_by_id(
            session, id_=user.uuid, data=UserUpdateSchema(password="new_password")
        )
        assert user_update.username == "test"
        assert user_update.email == "test@test.com"
        assert user_update.hashed_password == "drowssap_wen"

    async def test_update_user_conflict(self, session):
        _ = await UserCrud.create(
            session,
            UserInSchema(
                username="test",
                email="test@test.com",
                password="password",
            ),
        )
        _ = await UserCrud.create(
            session,
            UserInSchema(
                username="test1",
                email="test1@test.com",
                password="password",
            ),
        )

        with pytest.raises(IntegrityConflictException):
            _ = await UserCrud.update_by_id(
                session,
                id_="test1",
                column="username",
                data=UserUpdateSchema(email="test@test.com"),
            )
