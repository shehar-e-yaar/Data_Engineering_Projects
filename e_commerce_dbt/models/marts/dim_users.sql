select
    row_number() over (order by user_id) as user_key,
    user_id,
    full_name,
    email,
    country,
    signup_date
from {{ ref('stg_users') }}