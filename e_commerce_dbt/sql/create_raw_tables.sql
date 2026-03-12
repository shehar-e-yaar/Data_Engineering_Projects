-- Create warehouse
CREATE OR REPLACE WAREHOUSE ecommerce_wh
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- Create database
CREATE OR REPLACE DATABASE ecommerce_dw;

-- Create schemas
CREATE OR REPLACE SCHEMA ecommerce_dw.raw;
CREATE OR REPLACE SCHEMA ecommerce_dw.analytics;

-- Use raw schema
USE DATABASE ecommerce_dw;
USE SCHEMA raw;

-- Raw users table
CREATE OR REPLACE TABLE raw_users (
    user_id INTEGER,
    full_name STRING,
    email STRING,
    country STRING,
    signup_date DATE
);

-- Raw products table
CREATE OR REPLACE TABLE raw_products (
    product_id INTEGER,
    product_name STRING,
    category STRING,
    price NUMBER(10,2)
);

-- Raw orders table
CREATE OR REPLACE TABLE raw_orders (
    order_id INTEGER,
    user_id INTEGER,
    order_date DATE,
    status STRING
);

-- Raw order items table
CREATE OR REPLACE TABLE raw_order_items (
    order_item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price NUMBER(10,2)
);