from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from snippets.models.base import IdMixin, TimestampMixin


class UserBase(SQLModel):
    email: EmailStr = Field(
        nullable=False, index=True, sa_column_kwargs={"unique": True}
    )
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class User(IdMixin, TimestampMixin, UserBase, table=True):
    __tablename__ = "users"


class UserResponse(User, table=False):
    pass
