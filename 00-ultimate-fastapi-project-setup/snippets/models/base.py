from datetime import UTC, datetime
from uuid import UUID

from sqlmodel import Field, SQLModel
from uuid_extensions import uuid7


class IdMixin(SQLModel):
    id: UUID | None = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


def utc_now():
    return datetime.now(UTC).replace(tzinfo=None)


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(default_factory=utc_now, nullable=False)
    updated_at: datetime | None = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now()},
    )


class DeleteResponse(SQLModel):
    deleted: int
