import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI

from snippets.api.routes import router as api_router
from snippets.core.config import settings
from snippets.db.session import engine
from snippets.db.utils import create_db_and_tables

warnings.filterwarnings(
    "ignore", category=UserWarning, message=r".*PydanticJsonSchemaWarning.*"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(engine)
    yield


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()


@app.get("/", tags=["health"])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )
