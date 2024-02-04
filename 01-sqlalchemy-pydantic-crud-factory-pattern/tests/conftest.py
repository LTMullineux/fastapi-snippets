import asyncio

import pytest
import pytest_asyncio
from snippets.database import (
    Base,
    create_async_engine,
    create_extensions,
    create_pg_url_from_env,
)
from sqlalchemy.ext.asyncio import async_sessionmaker


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine(event_loop):
    url = create_pg_url_from_env()
    engine = create_async_engine(url, echo=False)
    await create_extensions(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    SessionLocal = async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        async with SessionLocal(bind=conn) as session:
            nested_tsx = await conn.begin_nested()
            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()

        await conn.close()
