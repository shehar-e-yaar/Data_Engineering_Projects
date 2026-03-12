select distinct
    to_number(to_char(order_date, 'YYYYMMDD')) as date_key,
    order_date as full_date,
    day(order_date) as day,
    month(order_date) as month,
    monthname(order_date) as month_name,
    quarter(order_date) as quarter,
    year(order_date) as year
from {{ ref('stg_orders') }}
where order_date is not null