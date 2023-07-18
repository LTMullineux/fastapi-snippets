from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from models.base import IdMixin, TimestampMixin


class UserBase(SQLModel):
    first_name: str = None
    last_name: str = None
    email: EmailStr = Field(
        nullable=False, index=True, sa_column_kwargs={"unique": True}
    )
    is_active: bool = True


class UserCreate(UserBase):
    ...


class UserUpdate(UserBase):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    is_active: bool = None


class User(IdMixin, TimestampMixin, UserBase, table=True):
    __tablename__ = "users"


class UserResponse(User, table=False):
    ...
