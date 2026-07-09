WITH source_books AS (
    SELECT * FROM library_db.books
),
source_authors AS (
    SELECT * FROM library_db.authors
),
source_book_authors AS (
    SELECT * FROM library_db.book_authors
)

SELECT
    b.id AS book_id,
    b.title,
    b.isbn,
    b.published_year,
    GROUP_CONCAT(a.first_name, ' ', a.last_name) AS author_name
FROM source_books b
INNER JOIN source_book_authors ba ON b.id = ba.book_id
INNER JOIN source_authors a ON ba.author_id = a.id
GROUP BY b.id, b.title, b.isbn, b.published_year