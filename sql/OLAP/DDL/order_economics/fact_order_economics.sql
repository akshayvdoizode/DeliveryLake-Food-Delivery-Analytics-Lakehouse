CREATE TABLE fact_order_economics (
    -- Degenerate dimension
    order_id BIGINT PRIMARY KEY,
    -- Dimension foreign keys (surrogate keys)
    restaurant_sk BIGINT NOT NULL,
    customer_sk BIGINT NOT NULL,
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
    -- Fact counters
    order_count INT DEFAULT 1,
    -- Flags
    is_payment_success INT,
    is_completed_order INT,
    is_cancelled_order INT,
    -- Audit timestamps
    order_created_time TIMESTAMP,
    payment_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Foreign key relationships
    CONSTRAINT fk_restaurant
        FOREIGN KEY (restaurant_sk)
        REFERENCES dim_restaurant(restaurant_sk),
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_sk)
        REFERENCES dim_customer(customer_sk),
    CONSTRAINT fk_order_date
        FOREIGN KEY (order_date_key)
        REFERENCES dim_date(date_key),
    CONSTRAINT fk_payment_date
        FOREIGN KEY (payment_date_key)
        REFERENCES dim_date(date_key)
);