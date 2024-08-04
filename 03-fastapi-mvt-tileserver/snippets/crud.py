from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from geoalchemy2.functions import (
    ST_AsMVT,
    ST_AsMVTGeom,
    ST_Intersects,
    ST_TileEnvelope,
    ST_Transform,
)
from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import literal

from snippets.models import Listing


@cached(
    ttl=600,
    cache=Cache.MEMORY,
    serializer=PickleSerializer(),
)
async def get_listing_tiles_bytes(
    session: AsyncSession,
    z: int,
    x: int,
    y: int,
    recently_active: bool | None = True,
) -> bytes | None:
    tile_bounds_cte = select(
        ST_TileEnvelope(z, x, y).label("geom_3857"),
        ST_Transform(ST_TileEnvelope(z, x, y), 4326).label("geom_4326"),
    ).cte("tile_bounds_cte")

    mvt_table_cte = (
        select(
            ST_AsMVTGeom(
                ST_Transform(Listing.geometry, 3857), tile_bounds_cte.c.geom_3857
            ).label("geom"),
            Listing.listing_id,
            Listing.longitude,
            Listing.latitude,
            Listing.property_type,
            Listing.property_sub_type,
            Listing.room_count,
            Listing.bathroom_count,
            Listing.sleep_count,
            Listing.rating,
            Listing.review_count,
            Listing.instant_book,
            Listing.is_superhost,
            Listing.is_hotel,
            Listing.children_allowed,
            Listing.events_allowed,
            Listing.smoking_allowed,
            Listing.pets_allowed,
            Listing.has_family_friendly,
            Listing.has_wifi,
            Listing.has_pool,
            Listing.has_air_conditioning,
            Listing.has_views,
            Listing.has_hot_tub,
            Listing.has_parking,
            Listing.has_patio_or_balcony,
            Listing.has_kitchen,
            Listing.nightly_price,
            Listing.name,
            Listing.main_image_url,
            Listing.recently_active,
        )
        .select_from(Listing)
        .join(tile_bounds_cte, literal(True))  # cross join
        .filter(
            and_(
                Listing.geometry.is_not(None),
                ST_Intersects(Listing.geometry, tile_bounds_cte.c.geom_4326),
            )
        )
    )

    if recently_active is not None:
        mvt_table_cte = mvt_table_cte.filter(Listing.recently_active == recently_active)

    mvt_table_cte = mvt_table_cte.cte("mvt_table_cte")
    stmt = select(ST_AsMVT(text("mvt_table_cte.*"))).select_from(mvt_table_cte)
    result = await session.execute(stmt)
    return result.scalar()
