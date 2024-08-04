from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from snippets.crud.user import create_user, delete_user, get_user, update_user
from snippets.db.session import get_session
from snippets.models.base import DeleteResponse
from snippets.models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    summary="Create a new user.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user_route(
    data: UserCreate,
    db: AsyncSession = Depends(get_session),
):
    return await create_user(session=db, user=data)


@router.get(
    "/{id}",
    summary="Get a user.",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def get_user_route(id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_user(session=db, id=id)


@router.patch(
    "/{id}",
    summary="Update a user.",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
async def update_user_route(
    id: UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_session),
):
    return await update_user(session=db, id=id, user=data)


@router.delete(
    "/{id}",
    summary="Delete a user.",
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponse,
)
async def delete_user_route(id: UUID, db: AsyncSession = Depends(get_session)):
    deleted = await delete_user(session=db, id=id)
    return DeleteResponse(deleted=deleted)
