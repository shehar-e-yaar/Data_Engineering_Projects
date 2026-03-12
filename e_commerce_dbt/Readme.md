# E-commerce Data Warehouse Project

## Overview

This project demonstrates how to build a simple end-to-end data warehouse for an e-commerce platform using modern data engineering tools.

The goal is to simulate transactional data and transform it into an analytics-ready star schema.

---

## Tech Stack

Python (Faker)
SQL
Snowflake
dbt
Dimensional Modeling

---

## Project Architecture

Python Faker
↓
CSV Data Generation
↓
Snowflake Raw Tables
↓
dbt Transformations
↓
Star Schema Data Warehouse
↓
Analytics Queries

---

## Data Model

Fact Table

fact_sales

Dimension Tables

dim_users
dim_products
dim_date

Star Schema:

        dim_users
           |
dim_products — fact_sales — dim_date

---

## Data Generation

Synthetic data is generated using Python and the Faker library.

Tables generated:

users
products
orders
order_items

---

## Transformations with dbt

dbt is used to transform raw tables into staging models and warehouse tables.

Staging models:

stg_users
stg_products
stg_orders
stg_order_items

Warehouse models:

dim_users
dim_products
dim_date
fact_sales

---

## Example Analytical Queries

### Monthly Revenue

```sql
SELECT
    d.year,
    d.month,
    SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d
ON f.date_key = d.date_key
GROUP BY d.year, d.month;