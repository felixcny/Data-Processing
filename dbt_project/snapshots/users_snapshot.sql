{% snapshot users_snapshot %}

{{
    config(
      target_schema='main_snapshots',
      unique_key='id_user',
      strategy='check',
      check_cols=['user_city', 'user_first_name', 'user_last_name'],
    )
}}

select 
    id_user,
    user_first_name,
    user_last_name,
    user_city
from {{ ref('stg_users') }}

{% endsnapshot %}