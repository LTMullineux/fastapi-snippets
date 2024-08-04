from os import environ

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from snippets.core.config import settings


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


url = create_pg_url_from_env(drivername="postgresql+asyncpg")
engine = create_async_engine(
    url,
    echo=settings.POSTGRES_ECHO,
    future=True,
    pool_size=max(5, settings.POSTGRES_POOL_SIZE),
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
