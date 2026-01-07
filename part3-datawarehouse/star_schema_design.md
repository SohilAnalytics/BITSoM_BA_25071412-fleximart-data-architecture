# Star Schema Design Documentation

## Section 1: Schema Overview

### FACT TABLE: fact_sales

**Grain:** One row per product per order line item
**Business Process:** Sales transactions

**Measures (Numeric Facts):**

* **quantity_sold:** Number of units sold per order line
* **unit_price:** Price per unit at the time of sale
* **discount_amount:** Discount applied on the order line
* **total_amount:** Final sales amount calculated as (quantity_sold × unit_price − discount_amount)

**Foreign Keys:**

* **date_key** → dim_date
* **product_key** → dim_product
* **customer_key** → dim_customer

The `fact_sales` table captures detailed transactional data at the lowest level, enabling accurate sales analysis across multiple dimensions.

---

### DIMENSION TABLE: dim_date

**Purpose:** Date dimension for time-based analysis
**Type:** Conformed dimension

**Attributes:**

* **date_key (PK):** Surrogate key in YYYYMMDD format
* **full_date:** Actual calendar date
* **day_of_week:** Monday, Tuesday, etc.
* **month:** Numeric month (1–12)
* **month_name:** January, February, etc.
* **quarter:** Q1, Q2, Q3, Q4
* **year:** Calendar year (e.g., 2023, 2024)
* **is_weekend:** Boolean flag indicating weekend

This dimension enables flexible reporting across different time hierarchies such as daily, monthly, quarterly, and yearly.

---

### D
