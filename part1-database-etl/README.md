Part 1: Database Design and ETL Pipeline
**Overview**

This part of the project was focused on building an ETL (Extract, Transform, Load) pipeline using Python for FlexiMart. The goal was to take raw CSV files containing customer, product, and sales data, clean the data, and load it into a relational database (MySQL).

After loading the data, the database schema was documented and SQL queries were written to answer specific business questions.

**Input Data**
-----

The ETL pipeline works with the following raw CSV files:

customers_raw.csv

Issues: missing emails, inconsistent phone formats, duplicate records

products_raw.csv

Issues: missing prices, inconsistent category names, null stock values

sales_raw.csv

Issues: inconsistent date formats, missing IDs, duplicate transactions
-----

**ETL Pipeline** (etl_pipeline.py)

The ETL process includes:

Extract

Reads all three CSV files using pandas

Transform

Removes duplicate records

Handles missing values using appropriate strategies

Standardizes phone number formats

Standardizes product category names

Converts dates to YYYY-MM-DD format

Prepares data for relational tables

Load

Inserts cleaned data into MySQL tables

Uses auto-incrementing primary keys

Includes basic error handling and logging
------

**Database Schema**

The cleaned data is loaded into the following tables:

customers

products

orders

order_items

Detailed schema documentation and relationships are explained in schema_documentation.md.
-----

**Business Queries**

SQL queries are written in business_queries.sql to answer business questions such as:

Customer purchase history

Product sales analysis

Monthly sales trends

**Data Quality Report**

The ETL pipeline generates data_quality_report.txt, which includes:

Number of records processed

Duplicates removed

Missing values handled

Records successfully loaded
