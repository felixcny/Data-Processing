{% snapshot products_snapshot %}

{{
    config(
      target_schema='main_snapshots',
      unique_key='id_product',
      strategy='check',
      check_cols=['product_price', 'product_category', 'product_title'],
    )
}}

select 
    id_product,
    product_title,
    product_price,
    product_category
from {{ ref('stg_products') }}

{% endsnapshot %}