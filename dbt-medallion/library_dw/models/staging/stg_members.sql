WITH source AS (
    SELECT * FROM library_db.members
)

SELECT
    id AS member_id,
    full_name AS member_name,
    email,
    phone_number,
    joined_date
FROM source