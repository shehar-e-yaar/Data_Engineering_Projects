select
    order_id,
    user_id,
    order_date,
    status
from {{ source('raw', 'raw_orders') }}