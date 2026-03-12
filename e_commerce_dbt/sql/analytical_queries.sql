-- Monthly revenue

SELECT
    d.year,
    d.month,
    SUM(f.total_amount) AS revenue
FROM analytics.fact_sales f
JOIN analytics.dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- Top 10 selling products

SELECT
    p.product_name,
    SUM(f.quantity) AS total_units_sold,
    SUM(f.total_amount) AS revenue
FROM analytics.fact_sales f
JOIN analytics.dim_products p
    ON f.product_key = p.product_key
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- Revenue by country

SELECT
    u.country,
    SUM(f.total_amount) AS revenue
FROM analytics.fact_sales f
JOIN analytics.dim_users u
    ON f.user_key = u.user_key
GROUP BY u.country
ORDER BY revenue DESC;

-- Top customers

SELECT
    u.full_name,
    SUM(f.total_amount) AS total_spent
FROM analytics.fact_sales f
JOIN analytics.dim_users u
    ON f.user_key = u.user_key
GROUP BY u.full_name
ORDER BY total_spent DESC
LIMIT 10;


--Revenue by product category

SELECT
    p.category,
    SUM(f.total_amount) AS revenue
FROM analytics.fact_sales f
JOIN analytics.dim_products p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;