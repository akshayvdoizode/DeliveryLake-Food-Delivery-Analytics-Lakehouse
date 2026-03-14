CREATE TABLE dim_restaurant (
    restaurant_key BIGSERIAL PRIMARY KEY,
    -- Business key from OLTP
    restaurant_id BIGINT NOT NULL,
    -- Descriptive attributes
    restaurant_name TEXT,
    cuisine TEXT,
    city TEXT,
    rating NUMERIC(3,2),
    popularity_score NUMERIC(5,2),
    -- Derived analytical attributes
    rating_bucket TEXT,
    -- Slowly changing dimension tracking
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    insert_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);