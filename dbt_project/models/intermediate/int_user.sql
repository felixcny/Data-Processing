WITH users_orders AS (
    SELECT
        cart_id_user as user_id,
        COUNT(id_cart) as nb_orders,
        SUM(cart_total) as total_revenue,
        AVG(cart_total) as avg_order_value
    FROM {{ref("stg_carts")}}
    GROUP BY 1
)

SELECT
    user_id,
    nb_orders,
    CAST(total_revenue AS float) as total_revenue,
    CAST(avg_order_value AS float) as avg_order_value,
    CASE
        WHEN nb_orders >= 10 THEN 'top_client'
        WHEN nb_orders >= 5 THEN 'regular_client'
        WHEN nb_orders >= 2 THEN 'casual_client'
        ELSE 'new_client'
    END as client_segment
FROM users_orders