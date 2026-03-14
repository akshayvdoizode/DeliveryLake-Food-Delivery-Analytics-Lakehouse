INSERT INTO warehouse_schema.dim_restaurant (
    restaurant_id,
    restaurant_name,
    city,
    cuisine,
    rating,
    popularity_score,
    rating_bucket,
    effective_start_date,
    effective_end_date,
    is_current,
    insert_ts
)
SELECT
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine,
    r.rating,
    r.popularity_score,
    CASE
        WHEN r.rating >= 4.5 THEN 'premium'
        WHEN r.rating >= 4.0 THEN 'high'
        WHEN r.rating >= 3.0 THEN 'average'
        ELSE 'low'
    END AS rating_bucket,
    CURRENT_DATE AS effective_start_date,
    DATE '9999-12-31' AS effective_end_date,
    TRUE AS is_current,
    CURRENT_TIMESTAMP AS insert_ts
FROM restaurants r;