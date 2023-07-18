from api.routes import router as api_router
from core.config import settings
from db.utils import create_db_and_tables
from db.session import engine
from fastapi import FastAPI


def get_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
    )
    app.include_router(api_router, prefix="/api")
    return app


app = get_application()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables(engine)


@app.get("/", tags=["health"])
async def health():
    return dict(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="OK",
        message="Visit /docs for more information.",
    )
