INSERT INTO warehouse_schema.dim_customer (
    customer_id,
    customer_name,
    city,
    signup_date,
    effective_start_date,
    effective_end_date,
    is_current,
    insert_ts
)
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.signup_date,
    c.signup_date AS effective_start_date,
    DATE '9999-12-31' AS effective_end_date,
    TRUE AS is_current,
    CURRENT_TIMESTAMP AS insert_ts
FROM customers c;