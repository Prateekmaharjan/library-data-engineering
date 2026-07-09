WITH stg_borrow AS (
    SELECT * FROM {{ ref('stg_borrow_records') }}
),
stg_books AS (
    SELECT * FROM {{ ref('stg_books') }}
),
dim_date AS (
    SELECT * FROM {{ ref('dim_date') }}
),
book_copies AS (
    SELECT * FROM library_db.book_copies
)

SELECT
    stg_borrow.borrow_id,
    stg_borrow.member_id,
    stg_books.book_id,
    dim_date.full_date AS borrowed_date,
    stg_borrow.days_borrowed,
    stg_borrow.is_returned,
    stg_borrow.is_overdue
FROM stg_borrow
INNER JOIN book_copies ON book_copies.id = stg_borrow.book_copy_id
INNER JOIN stg_books ON stg_books.book_id = book_copies.book_id
INNER JOIN dim_date ON dim_date.full_date = stg_borrow.borrowed_date