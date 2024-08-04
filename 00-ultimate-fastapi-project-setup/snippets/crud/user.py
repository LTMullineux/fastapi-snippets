from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select

from snippets.models.user import User, UserCreate, UserUpdate


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    db_user = User.model_validate(user)
    try:
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )


async def get_user(session: AsyncSession, id: UUID) -> User:
    query = select(User).where(User.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def update_user(session: AsyncSession, id: UUID, user: UserUpdate) -> User:
    db_user = await get_user(session, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for k, v in user.model_dump(exclude_unset=True).items():
        setattr(db_user, k, v)

    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Updated user collides with other users",
        )


async def delete_user(session: AsyncSession, id: UUID) -> int:
    query = delete(User).where(User.id == id)
    response = await session.execute(query)
    await session.commit()
    return response.rowcount
