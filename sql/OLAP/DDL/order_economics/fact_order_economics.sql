CREATE TABLE fact_order_economics (
    -- Degenerate dimension
    order_id BIGINT PRIMARY KEY,
    -- Dimension foreign keys
    restaurant_key BIGINT NOT NULL,
    customer_key BIGINT NOT NULL,
    -- Role playing date dimensions
    order_date_key INT NOT NULL,
    payment_date_key INT,
    -- Measures
    gross_order_value NUMERIC(12,2) NOT NULL,
    payment_amount NUMERIC(12,2) NOT NULL,
    refund_amount NUMERIC(12,2) NOT NULL,
    net_revenue NUMERIC(12,2) NOT NULL,
    -- Basket metrics
    total_items INT,
    distinct_items INT,
    order_processing_seconds INT,
    -- Counters
    order_count INT DEFAULT 1,
    -- Flags
    is_payment_success BOOLEAN,
    is_completed_order BOOLEAN,
    is_cancelled_order BOOLEAN,
    -- Operational timestamps
    order_created_time TIMESTAMP,
    payment_time TIMESTAMP,
    insert_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Foreign keys
    CONSTRAINT fk_restaurant
        FOREIGN KEY (restaurant_key)
        REFERENCES dim_restaurant(restaurant_key),
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_order_date
        FOREIGN KEY (order_date_key)
        REFERENCES dim_date(date_key),
    CONSTRAINT fk_payment_date
        FOREIGN KEY (payment_date_key)
        REFERENCES dim_date(date_key)
);