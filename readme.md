
# Food Delivery Data Warehouse

## Fact Table: `fact_order_economics`

## Overview

This project implements the **Gold layer fact table** for a Food Delivery analytics warehouse using a **Lakehouse architecture**.

The goal of this pipeline is to create a **single source of truth for order-level economics**, enabling analytical queries related to revenue, customer behavior, restaurant performance, and operational efficiency.

The warehouse follows a **dimensional modeling approach (Kimball methodology)** with a **1-row-per-order fact grain**.

---

# Architecture

Operational system:

```
Postgres OLTP
    ↓
Bronze Layer (raw ingestion)
    ↓
Silver Layer (cleaned operational tables)
    ↓
Gold Layer (analytics-ready dimensional model)
```

Fact tables and dimensions reside in the **Gold layer**.

---

# Fact Table: `fact_order_economics`

## Grain

**1 row per order**

Each record represents the economic outcome of a single order placed on the platform.

---

# Source Tables

Operational tables used to build the fact table:

| Table         | Purpose                         |
| ------------- | ------------------------------- |
| `orders`      | Order lifecycle information     |
| `order_items` | Item-level details              |
| `payments`    | Payment attempts and completion |
| `refunds`     | Refund transactions             |
| `customers`   | Customer attributes             |
| `restaurants` | Restaurant attributes           |

---

# Aggregation Logic

Three pre-aggregations are used to convert operational tables into order-level metrics.

### 1. Order Item Aggregation

Source: `order_items`

Metrics generated:

* `gross_order_value`
* `total_items`
* `distinct_items`

Logic:

```
SUM(quantity * unit_price)
SUM(quantity)
COUNT(*)
```

Purpose:

Transform item-level data into **order-level economic metrics**.

---

### 2. Payment Aggregation

Source: `payments`

Handled complexities:

* multiple payment attempts
* failed payment retries
* successful payment detection

Metrics generated:

* `payment_amount`
* `payment_time`
* `is_payment_success`

Logic:

Only payments with status **`paid`** contribute to revenue.

```
SUM(payment_amount where status = paid)
MAX(payment_time where status = paid)
```

The success flag is derived from the existence of at least one successful payment.

---

### 3. Refund Aggregation

Source: `refunds`

Metric generated:

* `refund_amount`

Logic:

```
SUM(refund_amount)
```

This represents the **total refunded value for an order**.

---

# Measures

| Column              | Description                     |
| ------------------- | ------------------------------- |
| `gross_order_value` | Total value of items ordered    |
| `payment_amount`    | Total successful payment amount |
| `refund_amount`     | Total refunded amount           |
| `net_revenue`       | payment_amount − refund_amount  |
| `total_items`       | Total quantity purchased        |
| `distinct_items`    | Number of unique items          |

---

# Operational Metrics

| Column                     | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `order_processing_seconds` | Time from order creation to payment completion |

Calculation:

```
payment_time - order_time
```

Converted into seconds.

---

# Role-Playing Date Dimensions

The fact table references the **date dimension multiple times**.

| Column             | Description                 |
| ------------------ | --------------------------- |
| `order_date_key`   | Date when order was created |
| `payment_date_key` | Date when payment completed |

Date keys follow the format:

```
YYYYMMDD
```

Example:

```
20250724
```

---

# Dimension Tables

The fact table references two dimensions.

## `dim_customer`

Type: **SCD Type 2**

Tracks historical changes in customer attributes.

Columns:

```
customer_key (surrogate key)
customer_id (business key)
effective_start_date
effective_end_date
is_current
```

---

## `dim_restaurant`

Type: **SCD Type 2**

Tracks restaurant attribute changes.

Columns:

```
restaurant_key (surrogate key)
restaurant_id (business key)
effective_start_date
effective_end_date
is_current
```

---

# Surrogate Key Resolution

Fact tables reference **surrogate keys instead of business keys**.

Lookups are performed using:

```
restaurant_id → restaurant_key
customer_id → customer_key
```

If the lookup fails, the **unknown dimension key (0)** is assigned.

```
COALESCE(dim_key, 0)
```

This prevents NULL foreign keys.

---

# Flags

Boolean flags simplify downstream BI queries.

| Column               | Description                                    |
| -------------------- | ---------------------------------------------- |
| `is_payment_success` | True if at least one successful payment exists |
| `is_completed_order` | Order completed successfully                   |
| `is_cancelled_order` | Order was cancelled                            |

These flags avoid repeated CASE logic in reporting queries.

---

# Revenue Calculation

Revenue metrics follow this formula:

```
gross_order_value
        ↓
payment_amount
        ↓
refund_amount
        ↓
net_revenue = payment_amount − refund_amount
```

This ensures refunds are properly deducted from platform revenue.

---

# Handling Late Data

Operational systems often produce late events such as:

* delayed payments
* post-order refunds

To handle this, the fact table is designed to support **upserts (MERGE)** rather than append-only inserts.

Existing orders can be updated when new financial events occur.

---

# Data Quality Protections

The pipeline includes safeguards for common issues.

### Prevent NULL dimension keys

```
COALESCE(dim_key, 0)
```

### Ensure revenue integrity

```
net_revenue = payment_amount − refund_amount
```

### Correct payment accounting

Only successful payments contribute to revenue.

---

# Analytical Use Cases

This fact table supports queries such as:

### Revenue analysis

```
Daily revenue
Revenue by restaurant
Revenue by city
```

### Customer analytics

```
Customer order frequency
Average order value
Customer lifetime value
```

### Operational efficiency

```
Order processing latency
Payment success rate
Cancellation rate
```

---

# Example Query

Total daily revenue:

```sql
SELECT
    order_date_key,
    SUM(net_revenue) AS total_revenue
FROM fact_order_economics
GROUP BY order_date_key
ORDER BY order_date_key;
```

---

# Future Enhancements

The model can be extended with additional facts such as:

```
fact_delivery
fact_driver_payout
fact_order_item
fact_order_status_events
```

Additional dimensions may include:

```
dim_driver
dim_location
dim_payment_method
```

These extensions enable deeper operational analytics for the delivery platform.

---

# Summary

This warehouse model provides a **clean, scalable representation of order economics**.

Key characteristics:

* Dimensional model using **Kimball methodology**
* Fact grain defined as **1 row per order**
* Financial correctness through **payment and refund aggregation**
* Historical tracking via **SCD Type 2 dimensions**
* Designed for **analytical workloads and BI reporting**

If you want, the next improvement would be turning this README into a **GitHub-grade project documentation structure** (architecture diagram, data flow diagram, folder layout, and pipeline orchestration). That’s what makes a portfolio repo look like something built by a senior data engineer rather than a tutorial project.


If someone asks about the restaurant effective start date vs customer signup date, the correct explanation is simple and logical.

The customer signup date represents a business event from the operational system, while the restaurant effective_start_date is part of the SCD Type 2 dimension tracking when that version of the record became active in the warehouse. These two timelines represent different concepts: entity lifecycle versus dimension version validity.