# FlexiMart Data Architecture Project

**Student Name:** Sohil Rakesh Shah
**Student ID:** BITSoM_BA_25071412
**Email:** emailfromsohilshah@gmail.com			
**Date:** 08/01/2026


## Project Overview

This project was completed as part of the AI Data Architecture assignment for FlexiMart, an e-commerce company. I built an ETL pipeline using Python to clean and load raw CSV data into a relational database, answered business questions using SQL and finally designed a data warehouse using a star schema for analytical reporting.

The project shows the complete flow of data from raw files to business insights.


## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 

## Setup Instructions

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


## Key Learnings

Through this assignment, I learned how to build a complete ETL pipeline using Python, handle real-world data quality issues, and work with relational databases using SQL.Additionally, I gained hands-on experience in data warehouse design, star schema modeling, and writing OLAP queries for business analysis.


## Challenges Faced

1. Handling data quality issues in CSV files – Solved by cleaning duplicates, fixing formats, and handling missing values in the ETL pipeline.
2. Designing analytical queries and warehouse schema – Solved by understanding business requirements and applying proper grouping, joins, and dimensional modeling.

