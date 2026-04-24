WITH SOURCE AS (
    SELECT * FROM {{ source('raw_data', 'carts') }}
)

SELECT 
    id_cart,
    id_user as cart_id_user,
    products as cart_products,
    CAST(total as float) as cart_total,
FROM SOURCE