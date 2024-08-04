#!/bin/bash

# Directory containing your gzip CSV files
DATA_DIR="/docker-entrypoint-initdb.d/data"

# Loop through all gzip files in the data directory
for file in "$DATA_DIR"/*.gz; do
    echo "Loading data from $file into listing ..."
    gzip -dc "$file" | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "COPY listing ( listing_id, longitude, latitude, property_type, property_sub_type, room_count, bathroom_count, sleep_count, rating, review_count, instant_book, is_superhost, is_hotel, children_allowed, events_allowed, smoking_allowed, pets_allowed, has_family_friendly, has_wifi, has_pool, has_air_conditioning, has_views, has_hot_tub, has_parking, has_patio_or_balcony, has_kitchen, nightly_price, name, main_image_url, recently_active ) FROM STDIN DELIMITER ',' CSV HEADER"
done

echo "Data loading complete."
