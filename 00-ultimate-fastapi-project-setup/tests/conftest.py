from typing import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from snippets.db.session import create_pg_url_from_env, get_session


@pytest_asyncio.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    url = create_pg_url_from_env()
    engine = create_async_engine(
        url,
        echo=False,
        future=True,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        try:
            async with SessionLocal(bind=conn) as session:
                nested_tsx = await conn.begin_nested()
                yield session

                if nested_tsx.is_active:
                    await nested_tsx.rollback()

                await tsx.rollback()
        finally:
            await tsx.close()

        await conn.close()


class BaseTestRouter:
    router = None

    @pytest_asyncio.fixture(scope="function")
    async def client(self, session):
        app = FastAPI()
        app.include_router(self.router)
        app.dependency_overrides[get_session] = lambda: session

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c
