WITH SOURCE AS (
    SELECT * FROM {{ source('raw_data', 'users') }}
)

SELECT 
    id_user,
    firstname as user_first_name,
    lastname as user_last_name,
    gender as user_gender,
    birthdate as user_birth_date,
    address.address as user_address,
    address.city as user_city,
    address.state as user_state,
    address.stateCode as user_state_code,
    address.postalCode as user_postal_code,
    address.coordinates as user_coordinates,
    address.country as user_country,
    role as user_role
FROM SOURCE