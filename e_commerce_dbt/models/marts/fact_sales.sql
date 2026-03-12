select
    oi.order_item_id as sales_key,
    o.order_id,
    u.user_key,
    p.product_key,
    to_number(to_char(o.order_date, 'YYYYMMDD')) as date_key,
    oi.quantity,
    oi.unit_price,
    oi.quantity * oi.unit_price as total_amount
from {{ ref('stg_order_items') }} oi
join {{ ref('stg_orders') }} o
    on oi.order_id = o.order_id
join {{ ref('dim_users') }} u
    on o.user_id = u.user_id
join {{ ref('dim_products') }} p
    on oi.product_id = p.product_id