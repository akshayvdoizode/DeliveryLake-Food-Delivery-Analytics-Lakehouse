CREATE TABLE dim_customer (
    -- Surrogate key
    customer_KEY BIGSERIAL PRIMARY KEY,
    -- Business key from OLTP
    customer_id BIGINT NOT NULL,
    -- Descriptive attributes
    customer_name TEXT,
    city TEXT,
    signup_date DATE,
    -- Slowly changing dimension tracking
    effective_start_date DATE NOT NULL,
    effective_end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL,
    insert_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);