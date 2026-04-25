{{ config(materialized='table') }}

WITH user_info AS (
    SELECT
        *
    FROM {{ ref('stg_users') }}
),

user_kpis AS (
    SELECT
        *
    FROM {{ ref('int_user') }}
)

SELECT
    u.id_user,
    u.user_first_name,
    u.user_last_name,
    u.user_first_name || ' ' || u.user_last_name as user_full_name,
    u.user_city,
    u.user_state,
    u.user_country,
    date_diff('year', u.user_birth_date, current_date) as user_age,
    CASE
        WHEN user_age < 25 THEN 'Etudiant'
        WHEN user_age >= 25 AND user_age < 35 THEN 'Jeune actif'
        WHEN user_age >= 35 AND user_age < 50 THEN 'Actif'
        WHEN user_age >= 50 AND user_age < 65 THEN 'Senior'
        ELSE 'Retraité'
    END AS age_segment,
    COALESCE(k.nb_orders, 0) as nb_orders,
    COALESCE(CAST(k.total_revenue AS float), 0.0) as total_revenue,
    COALESCE(CAST(k.avg_order_value AS float), 0.0) as avg_order_value,
    COALESCE(k.client_segment, 'nouveau_client') as client_segment
FROM user_info u
LEFT JOIN user_kpis k 
    ON u.id_user = k.user_id

    