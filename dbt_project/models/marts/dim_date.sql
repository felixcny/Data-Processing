{{ config(materialized='table') }}

WITH date_spine AS (
    SELECT 
        CAST(range AS DATE) AS date_day
    FROM range(DATE '2025-01-01', DATE '2026-01-01', INTERVAL '1 day')
)

SELECT
    CAST(strftime(date_day, '%Y%m%d') AS INTEGER) AS date_id,
    date_day AS full_date,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    strftime(date_day, '%B') AS month_name,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(DOW FROM date_day) AS day_of_week,
    strftime(date_day, '%A') AS day_name,
    CASE WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend,
    EXTRACT(QUARTER FROM date_day) AS quarter
FROM date_spine