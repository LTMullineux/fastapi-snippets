import gzip

from fastapi import Depends, FastAPI, Path, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from snippets.config import config
from snippets.crud import get_listing_tiles_bytes
from snippets.db import get_session

templates = Jinja2Templates(directory="./snippets/templates")


async def tile_args(
    z: int = Path(..., ge=0, le=24),
    x: int = Path(..., ge=0),
    y: int = Path(..., ge=0),
) -> dict[str, str]:
    return dict(z=z, x=x, y=y)


app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": config.PROJECT_NAME,
            "host": "localhost",
            "port": config.SNIPPETS_PORT,
            "mapbox_access_token": config.MAPBOX_ACCESS_TOKEN,
        },
    )


@app.get(
    "/listings/tiles/{z}/{x}/{y}.mvt",
    summary="Get listing tiles",
)
async def get_listing_tiles(
    tile: dict[str, int] = Depends(tile_args),
    session: AsyncSession = Depends(get_session),
) -> Response:
    byte_tile = await get_listing_tiles_bytes(
        session=session, recently_active=True, **tile
    )
    byte_tile = b"" if byte_tile is None else byte_tile
    return Response(
        content=gzip.compress(byte_tile),
        media_type="application/vnd.mapbox-vector-tile",
        headers={"Content-Encoding": "gzip"},
        status_code=status.HTTP_200_OK,
    )
