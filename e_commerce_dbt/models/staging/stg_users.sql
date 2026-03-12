select
    user_id,
    full_name,
    email,
    country,
    signup_date
from {{ source('raw', 'raw_users') }}