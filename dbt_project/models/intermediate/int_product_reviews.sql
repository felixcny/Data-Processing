WITH unnest_review AS (
    SELECT 
        id_product,
        unnest(product_reviews) as review
    FROM {{ ref('stg_products') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['id_product', 'review.reviewerEmail', 'review.date', 'review.comment']) }} AS review_id,
    id_product,
    CAST(review.rating as INT) as review_rating,
    review.comment as review_comment,
    CAST(review.date as TIMESTAMP) as review_date,
    review.reviewerName as review_reviewer_name,
    review.reviewerEmail as review_reviewer_email
FROM unnest_review