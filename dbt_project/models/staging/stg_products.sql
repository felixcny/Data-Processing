WITH SOURCE AS (
    SELECT * FROM {{ source('raw_data', 'products') }}
)

SELECT 
    id_product,
    title as product_title,
    description as product_description,
    category as product_category,
    CAST(price as float) as product_price,
    CAST(discount_percentage as float) as product_discount_percentage,
    CAST(rating as float) as product_rating,
    CAST(stock as int) as product_stock_quantity,
    reviews as product_reviews,
    availability_status as product_availability_status
FROM SOURCE