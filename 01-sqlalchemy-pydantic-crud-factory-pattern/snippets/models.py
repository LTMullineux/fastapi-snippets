from datetime import datetime
from typing import TypeAlias
from uuid import UUID as UuidType

from pydantic import BaseModel
from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as UuidColumn
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import FunctionElement
from uuid6 import uuid7

from snippets.database import Base

# Some generic types for the SQLAlchemy and Pydantic models
SnippetModel: TypeAlias = Base
SnippetSchema: TypeAlias = BaseModel


# some mixins to make our life easier
class UuidMixin:
    uuid: Mapped[UuidType] = mapped_column(
        "uuid",
        UuidColumn(as_uuid=True),
        primary_key=True,
        default=uuid7,
        nullable=False,
        sort_order=-1000,
    )


class UuidMixinSchema(BaseModel):
    uuid: UuidType = None


class utcnow(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=utcnow(),
        sort_order=9999,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
        server_default=utcnow(),
        server_onupdate=utcnow(),
        sort_order=10000,
    )


class TimestampMixinSchema(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None


# now the real models
# first posts
class Post(Base, UuidMixin, TimestampMixin):
    __tablename__ = "post"

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False, server_default="False")
    views: Mapped[int] = mapped_column(nullable=False, server_default="0")


class PostSchema(UuidMixinSchema, TimestampMixinSchema):
    title: str
    content: str
    published: bool = False
    views: int = 0


class PostUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    views: int | None = None


# the users
class User(Base, UuidMixin, TimestampMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="TRUE")


class UserBaseSchema(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserSchema(UserBaseSchema, UuidMixinSchema, TimestampMixinSchema):
    hashed_password: str


class UserInSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
