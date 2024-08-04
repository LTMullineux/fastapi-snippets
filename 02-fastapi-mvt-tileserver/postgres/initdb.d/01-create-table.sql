CREATE TABLE listing (
    listing_id VARCHAR PRIMARY KEY,
    longitude DOUBLE PRECISION NULL,
    latitude DOUBLE PRECISION NULL,
    geometry public.geometry(point, 4326) GENERATED ALWAYS AS (
        st_setsrid(st_makepoint(longitude, latitude), 4326)
    ) STORED NULL,
    property_type VARCHAR NULL,
    property_sub_type VARCHAR NULL,
    room_count INTEGER NULL,
    bathroom_count INTEGER NULL,
    sleep_count INTEGER NULL,
    rating DOUBLE PRECISION NULL,
    review_count INTEGER NULL,
    instant_book BOOLEAN NULL,
    is_superhost BOOLEAN NULL,
    is_hotel BOOLEAN NULL,
    children_allowed BOOLEAN NULL,
    events_allowed BOOLEAN NULL,
    smoking_allowed BOOLEAN NULL,
    pets_allowed BOOLEAN NULL,
    has_family_friendly BOOLEAN NULL,
    has_wifi BOOLEAN NULL,
    has_pool BOOLEAN NULL,
    has_air_conditioning BOOLEAN NULL,
    has_views BOOLEAN NULL,
    has_hot_tub BOOLEAN NULL,
    has_parking BOOLEAN NULL,
    has_patio_or_balcony BOOLEAN NULL,
    has_kitchen BOOLEAN NULL,
    nightly_price INTEGER NULL,
    "name" TEXT NULL,
    main_image_url TEXT NULL,
    recently_active BOOLEAN NULL
);