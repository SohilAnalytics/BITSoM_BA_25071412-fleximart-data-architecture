**Overview**

This part of the project focuses on building a data warehouse for FlexiMart to analyze historical sales data. 
A star schema was designed to support analytical queries, and sample data was loaded to simulate real sales transactions. 
Using this warehouse, OLAP-style SQL queries were written to generate business insights.

**Star Schema Design**

The data warehouse follows a star schema with one fact table and multiple dimension tables.

Fact Table

fact_sales

Stores sales transactions at the order line-item level

Measures include quantity sold, unit price, discount, and total amount

Dimension Tables

dim_date – supports time-based analysis (day, month, quarter, year)

dim_product – contains product details such as category and price

dim_customer – stores customer information and segmentation data

The detailed design and reasoning are documented in star_schema_design.md.

-------------------------------------------------------------------------

**Warehouse Schema Implementation**

The warehouse schema is created using warehouse_schema.sql, following the provided structure exactly.
Sample data is inserted using warehouse_data.sql, which includes:

30 dates (January–February 2024)

15 products across 3 categories

12 customers from different cities

40 sales transactions with realistic patterns

-----------------------------------------------------------------------

OLAP Analytics

Analytical SQL queries are written in analytics_queries.sql to support decision-making, including:

Monthly sales drill-down (Year → Quarter → Month)

Top 10 products by revenue with contribution percentage

Customer segmentation based on total spending

These queries demonstrate OLAP concepts like aggregation, drill-down, and segmentation.

---------------------------------------------------------------------------

This part shows how raw transactional data can be transformed into a structured data warehouse that supports reporting and business analysis.
