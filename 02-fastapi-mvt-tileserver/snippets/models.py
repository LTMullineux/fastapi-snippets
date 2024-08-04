from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import Computed, Index
from sqlalchemy.orm import Mapped, mapped_column

from snippets.db import Base


class Listing(Base):
    __tablename__ = "listing"
    __table_args__ = (Index(None, "geometry", postgresql_using="gist"),)

    listing_id: Mapped[str] = mapped_column(primary_key=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=True)
    geometry: Mapped[Any] = mapped_column(
        Geometry(
            "POINT",
            srid=4326,
            spatial_index=False,
            from_text="ST_GeogFromText",
            name="geometry",
        ),
        Computed(
            """
                public.geometry(point, 4326) GENERATED ALWAYS AS (
                    st_setsrid(st_makepoint(longitude, latitude), 4326)
                )
            """,
            persisted=True,
        ),
        nullable=True,
    )
    property_type: Mapped[str] = mapped_column(nullable=True, index=True)
    property_sub_type: Mapped[str] = mapped_column(nullable=True, index=True)
    room_count: Mapped[int] = mapped_column(nullable=True, index=True)
    bathroom_count: Mapped[int] = mapped_column(nullable=True, index=True)
    sleep_count: Mapped[int] = mapped_column(nullable=True, index=True)
    rating: Mapped[float] = mapped_column(nullable=True, index=True)
    review_count: Mapped[int] = mapped_column(nullable=True, index=True)
    instant_book: Mapped[bool] = mapped_column(nullable=True, index=True)
    is_superhost: Mapped[bool] = mapped_column(nullable=True, index=True)
    is_hotel: Mapped[bool] = mapped_column(nullable=True, index=True)
    children_allowed: Mapped[bool] = mapped_column(nullable=True, index=True)
    events_allowed: Mapped[bool] = mapped_column(nullable=True, index=True)
    smoking_allowed: Mapped[bool] = mapped_column(nullable=True, index=True)
    pets_allowed: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_family_friendly: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_wifi: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_pool: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_air_conditioning: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_views: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_hot_tub: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_parking: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_patio_or_balcony: Mapped[bool] = mapped_column(nullable=True, index=True)
    has_kitchen: Mapped[bool] = mapped_column(nullable=True, index=True)
    nightly_price: Mapped[int] = mapped_column(nullable=True, index=True)
    name: Mapped[str] = mapped_column(nullable=True)
    main_image_url: Mapped[str] = mapped_column(nullable=True)
    recently_active: Mapped[bool] = mapped_column(nullable=True, index=True)
