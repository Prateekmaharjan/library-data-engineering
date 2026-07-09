WITH stg_members AS (
    SELECT * FROM {{ ref('stg_members') }}
)

SELECT
    member_id,
    member_name,
    email,
    phone_number,
    joined_date
FROM stg_members