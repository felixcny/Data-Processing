WITH sales_stats AS (
    SELECT
        product_id,
        SUM(product_quantity) AS total_qty_sold,
        SUM(product_total) AS total_revenu_sold
    FROM {{ ref("int_cart_items") }}
    GROUP BY 1
),

review_stats AS (
    SELECT
        id_product,
        AVG(review_rating) as avg_rating,
        COUNT(review_id) as nb_reviews,
    FROM {{ref("int_product_reviews")}}
    GROUP BY 1
)

SELECT
    COALESCE(s.product_id, r.id_product) AS product_id,
    COALESCE(s.total_qty_sold, 0) AS total_qty_sold,
    CAST(COALESCE(s.total_revenu_sold, 0) AS DECIMAL(10,2)) AS total_revenue_sold,
    CAST(r.avg_rating AS DECIMAL(10,2)) AS avg_rating,
    COALESCE(r.nb_reviews, 0) AS nb_reviews
FROM sales_stats s
FULL OUTER JOIN review_stats r ON s.product_id = r.id_product