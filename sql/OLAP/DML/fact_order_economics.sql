WITH items_agg AS (
    SELECT
        order_id,
        COUNT(*) AS distinct_items, -- number of unique line items in the order
        SUM(quantity * unit_price) AS gross_order_value, -- total order value before refunds
        SUM(quantity) AS total_items -- total quantity of items purchased
    FROM order_items
    GROUP BY order_id
),
payments_agg AS (
    SELECT
        order_id,
        -- sum only successful payments to avoid counting failed payment attempts
        SUM(CASE WHEN payment_status='paid'
                 THEN payment_amount ELSE 0 END) AS payment_amount,
        -- latest successful payment timestamp represents payment completion
        MAX(CASE WHEN payment_status='paid'
                 THEN payment_time END) AS payment_time,
        -- derive payment success flag (true if at least one successful payment exists)
        CASE
            WHEN SUM(CASE 
                        WHEN payment_status = 'paid' 
                        THEN 1 
                        ELSE 0 
                     END) > 0 
            THEN true 
            ELSE false 
        END AS is_payment_success
    FROM payments
    GROUP BY order_id
),
refunds_agg AS (
    SELECT
        order_id,
        -- aggregate all refunds issued for the order
        SUM(refund_amount) AS refund_amount

    FROM refunds
    GROUP BY order_id
)
SELECT
    o.order_id,
    -- surrogate key resolution for dimensions
    -- COALESCE handles late-arriving dimensions by assigning unknown key (0)
    COALESCE(dr.restaurant_key,0) AS restaurant_key,
    COALESCE(dc.customer_key,0) AS customer_key,
    -- role-playing date dimensions derived from timestamps
    TO_CHAR(o.order_time,'YYYYMMDD')::INT AS order_date_key,
    TO_CHAR(p.payment_time,'YYYYMMDD')::INT AS payment_date_key,
    -- timestamps retained for operational analysis
    o.order_time,
    p.payment_time,
    -- duration between order creation and payment completion
    -- NULL payment times are converted to 0
    coalesce(EXTRACT(EPOCH FROM (p.payment_time - o.order_time)),0) 
        as order_processing_seconds,
    -- order economic measures
    ig.gross_order_value,
    ig.total_items,
    ig.distinct_items,
    -- payment and refund measures
    COALESCE(p.payment_amount,0) AS payment_amount,
    COALESCE(rg.refund_amount,0) AS refund_amount,
    -- net revenue calculation
    COALESCE(p.payment_amount,0) - COALESCE(rg.refund_amount,0) 
        AS net_revenue,
    -- payment success indicator
    p.is_payment_success,
    -- order lifecycle flags
    CASE WHEN o.order_status='completed' THEN true ELSE false END 
        AS is_completed_order,
    CASE WHEN o.order_status='cancelled' THEN true ELSE false END 
        AS is_cancelled_order
FROM orders o
-- pre-aggregated item metrics
LEFT JOIN items_agg ig 
ON o.order_id = ig.order_id
-- aggregated payment information
LEFT JOIN payments_agg p 
ON o.order_id = p.order_id
-- aggregated refunds
LEFT JOIN refunds_agg rg 
ON o.order_id = rg.order_id
-- dimension lookup for restaurant
-- currently joining on is_current (initial load assumption)
LEFT JOIN warehouse_schema.dim_restaurant dr
ON o.restaurant_id = dr.restaurant_id 
AND dr.is_current
-- dimension lookup for customer
-- currently joining on is_current (SCD history not yet applied)
LEFT JOIN warehouse_schema.dim_customer dc
ON o.customer_id = dc.customer_id 
AND dc.is_current;