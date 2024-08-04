from os import environ
from typing import TypeAlias

import orjson
from pydantic import BaseModel
from sqlalchemy import MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import DeclarativeBase

from snippets.config import config


def orjson_serializer(obj):
    """
    Note that `orjson.dumps()` return byte array,
    while sqlalchemy expects string, thus `decode()` call.
    """
    return orjson.dumps(
        obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC
    ).decode()


naming_convention = {
    "ix": "ix_snippets_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_snippets_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_snippets_%(table_name)s_%(constraint_name)s",
    "fk": "fk_snippets_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_snippets_%(table_name)s",
}


class Base(DeclarativeBase, AsyncAttrs):
    metadata = MetaData(naming_convention=naming_convention)


SnippetModel: TypeAlias = Base
SnippetSchema: TypeAlias = BaseModel


def create_pg_url(
    drivername: str = "postgresql",
    username: str = "postgres",
    password: str = "postgres",
    host: str = "localhost",
    port: str = "5432",
    database: str = "postgres",
) -> URL:
    return URL.create(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def create_pg_url_from_env(
    drivername: str | None = None,
    username: str | None = None,
    password: str | None = None,
    host: str | None = None,
    port: str | None = None,
    database: str | None = None,
) -> URL:
    return create_pg_url(
        drivername=drivername or environ.get("POSTGRES_DRIVERNAME", "postgresql"),
        username=username or environ.get("POSTGRES_USER", "postgres"),
        password=password or environ.get("POSTGRES_PASSWORD", "postgres"),
        host=host or environ.get("POSTGRES_HOST", "localhost"),
        port=port or environ.get("POSTGRES_PORT", "5432"),
        database=database or environ.get("POSTGRES_DB", "postgres"),
    )


def create_async_engine(url: URL, **kwargs) -> AsyncEngine:
    return _create_async_engine(
        url,
        json_serializer=orjson_serializer,
        json_deserializer=orjson.loads,
        future=True,
        **kwargs,
    )


async def create_db_and_tables_async(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


url = create_pg_url_from_env(drivername="postgresql+asyncpg")
engine = create_async_engine(
    url,
    echo=False,
    pool_size=max(5, config.POSTGRES_POOL_SIZE),
    max_overflow=2 * max(5, config.POSTGRES_POOL_SIZE),
    pool_pre_ping=True,
    pool_recycle=900,
    pool_timeout=60,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
