{{config(materialized='table')}}

WITH product_info as (
    select * from {{ref('stg_products')}}
),

product_kpis as (
    select * from {{ref('int_product_kpis')}}
)

select
    p.id_product as product_id,
    p.product_title as product_title,
    p.product_category as product_category,
    p.product_description as product_description,
    CAST(p.product_price AS float) AS product_price,
    COALESCE(k.total_qty_sold, 0) AS total_qty_sold,
    CAST(COALESCE(k.total_revenue_sold, 0) AS DECIMAL(10,2)) AS total_revenue_sold,
    CAST(COALESCE(k.avg_rating, 0) AS DECIMAL(10,2)) AS avg_rating,
    COALESCE(k.nb_reviews, 0) AS nb_reviews,
    CASE
        WHEN k.avg_rating >= 4.5 THEN 'Excellent'
        WHEN k.avg_rating >= 4 THEN 'Good'
        WHEN k.avg_rating >= 3 THEN 'Average'
        WHEN k.avg_rating >= 2 THEN 'Poor'
        ELSE 'Very Poor'
    END AS rating_category,
    p.product_stock_quantity,
    p.product_availability_status,
from product_info p
left join product_kpis k on p.id_product = k.product_id