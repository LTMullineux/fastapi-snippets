from sqlmodel import SQLModel, Field
from uuid import UUID
from uuid_extensions import uuid7
from datetime import datetime


class IdMixin(SQLModel):
    id: UUID = Field(
        default_factory=uuid7,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class DeleteResponse(SQLModel):
    deleted: int
