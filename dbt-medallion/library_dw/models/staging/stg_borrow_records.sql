WITH source AS (
    SELECT * FROM library_db.borrow_records
)

SELECT
    id AS borrow_id,
    member_id,
    book_copy_id,
    borrowed_date,
    due_date,
    returned_date,
    CASE 
        WHEN returned_date IS NOT NULL 
        THEN DATEDIFF(returned_date, borrowed_date) 
        ELSE 0 
    END AS days_borrowed,
    CASE 
        WHEN returned_date IS NOT NULL THEN 1 
        ELSE 0 
    END AS is_returned,
    CASE 
        WHEN due_date < CURRENT_DATE AND returned_date IS NULL THEN 1 
        ELSE 0 
    END AS is_overdue
FROM source