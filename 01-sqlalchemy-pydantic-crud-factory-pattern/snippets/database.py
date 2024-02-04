from os import environ

from sqlalchemy import MetaData
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import text

EXTENSIONS = ["uuid-ossp", "postgis", "postgis_topology"]


naming_convention = {
    "ix": "ix_ct_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_ct_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_ct_%(table_name)s_%(constraint_name)s",
    "fk": "fk_ct_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_ct_%(table_name)s",
}


class Base(DeclarativeBase, AsyncAttrs):
    metadata = MetaData(naming_convention=naming_convention)


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
        database=database or environ.get("POSTGRES_DATABASE", "postgres"),
    )


def create_engine(url: URL, **kwargs) -> Engine:
    return _create_engine(url, **kwargs)


def create_async_engine(url: URL, **kwargs) -> AsyncEngine:
    pool_size_env = environ.get("POSTGRES_POOL_SIZE", 5)
    pool_size = int(kwargs.pop("pool_size", pool_size_env))
    return _create_async_engine(
        url,
        future=True,
        pool_size=pool_size,
        **kwargs,
    )


async def create_db_and_tables_async(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def create_db_and_tables_sync(engine: Engine):
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


async def create_extensions(engine):
    async with engine.connect() as conn:
        for extension in EXTENSIONS:
            await conn.execute(text(f'CREATE EXTENSION IF NOT EXISTS "{extension}"'))
