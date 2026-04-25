WITH extract_product AS (
    SELECT 
        id_cart,
        cart_id_user,
        unnest(cart_products) as product
    FROM {{ ref('stg_carts') }}
),

aggregated_product AS (
    SELECT 
        id_cart,
        cart_id_user,
        product.id as product_id,
        product.title as product_title,
        SUM(CAST(product.quantity as INT)) as product_quantity,
        AVG(CAST(product.price as DECIMAL(10,2))) as product_price,
        SUM(CAST(product.total as DECIMAL(10,2))) as product_total,
        AVG(CAST(product.discountPercentage as DECIMAL(10,2))) as product_discount_percentage,
        SUM(CAST(product.discountedTotal as DECIMAL(10,2))) as product_discounted_total
    FROM extract_product
    GROUP BY id_cart, cart_id_user, product.id, product.title
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['id_cart', 'product_id']) }} AS cart_item_id,
    *
FROM aggregated_product