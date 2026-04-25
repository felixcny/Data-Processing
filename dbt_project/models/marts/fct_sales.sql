{{ config(materialized = 'table') }}


with cart_items as (
    select * from {{ ref('int_cart_items') }}
),

valid_users as (
    select id_user from {{ ref('dim_user') }}
)

select 
    c.cart_item_id,
    c.id_cart as order_id,
    c.product_id,
    c.cart_id_user as user_id,
    c.product_quantity as quantity,
    CAST(strftime(c.sale_date, '%Y%m%d') as int) as date_id,
    c.sale_date,
    CAST(c.product_price AS DECIMAL(10,2)) as price,
    CAST(c.product_total AS DECIMAL(10,2)) as total,
    CAST(c.product_discounted_total AS DECIMAL(10,2)) as revenue_net,
    CAST(c.product_total - c.product_discounted_total AS DECIMAL(10,2)) as total_discount
FROM cart_items c
INNER JOIN valid_users v 
    ON c.cart_id_user = v.id_user



    