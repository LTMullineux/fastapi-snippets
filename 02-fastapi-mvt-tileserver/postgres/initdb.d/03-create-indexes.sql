CREATE INDEX ix_snippets_listing_property_type ON listing USING BTREE (property_type);
CREATE INDEX ix_snippets_listing_geometry ON listing USING GIST (geometry);
CREATE INDEX ix_snippets_listing_property_sub_type ON listing USING BTREE (property_sub_type);
CREATE INDEX ix_snippets_listing_room_count ON listing USING BTREE (room_count);
CREATE INDEX ix_snippets_listing_bathroom_count ON listing USING BTREE (bathroom_count);
CREATE INDEX ix_snippets_listing_sleep_count ON listing USING BTREE (sleep_count);
CREATE INDEX ix_snippets_listing_rating ON listing USING BTREE (rating);
CREATE INDEX ix_snippets_listing_review_count ON listing USING BTREE (review_count);
CREATE INDEX ix_snippets_listing_instant_book ON listing USING BTREE (instant_book);
CREATE INDEX ix_snippets_listing_is_superhost ON listing USING BTREE (is_superhost);
CREATE INDEX ix_snippets_listing_is_hotel ON listing USING BTREE (is_hotel);
CREATE INDEX ix_snippets_listing_children_allowed ON listing USING BTREE (children_allowed);
CREATE INDEX ix_snippets_listing_events_allowed ON listing USING BTREE (events_allowed);
CREATE INDEX ix_snippets_listing_smoking_allowed ON listing USING BTREE (smoking_allowed);
CREATE INDEX ix_snippets_listing_pets_allowed ON listing USING BTREE (pets_allowed);
CREATE INDEX ix_snippets_listing_has_family_friendly ON listing USING BTREE (has_family_friendly);
CREATE INDEX ix_snippets_listing_has_wifi ON listing USING BTREE (has_wifi);
CREATE INDEX ix_snippets_listing_has_pool ON listing USING BTREE (has_pool);
CREATE INDEX ix_snippets_listing_has_air_conditioning ON listing USING BTREE (has_air_conditioning);
CREATE INDEX ix_snippets_listing_has_views ON listing USING BTREE (has_views);
CREATE INDEX ix_snippets_listing_has_hot_tub ON listing USING BTREE (has_hot_tub);
CREATE INDEX ix_snippets_listing_has_parking ON listing USING BTREE (has_parking);
CREATE INDEX ix_snippets_listing_has_patio_or_balcony ON listing USING BTREE (has_patio_or_balcony);
CREATE INDEX ix_snippets_listing_has_kitchen ON listing USING BTREE (has_kitchen);
CREATE INDEX ix_snippets_listing_nightly_price ON listing USING BTREE (nightly_price);
CREATE INDEX ix_snippets_listing_recently_active ON listing USING BTREE (recently_active);
ANALYZE listing;