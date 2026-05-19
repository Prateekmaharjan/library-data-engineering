-- available copies of books
SELECT b.title, bc.id AS copy_id
FROM books b
JOIN book_copies bc ON b.id = bc.book_id
WHERE bc.is_available = TRUE
ORDER BY b.title;


-- overdue borrowed books
SELECT m.full_name, b.title, br.borrowed_date, br.due_date
FROM borrow_records br
JOIN members m ON br.member_id = m.id
JOIN book_copies bc ON br.book_copy_id = bc.id
JOIN books b ON bc.book_id = b.id
WHERE br.returned_date IS NULL
  AND br.due_date < CURRENT_DATE
ORDER BY br.due_date;


-- borrowing history of a member
SELECT m.full_name, b.title, br.borrowed_date, br.returned_date
FROM borrow_records br
JOIN members m ON br.member_id = m.id
JOIN book_copies bc ON br.book_copy_id = bc.id
JOIN books b ON bc.book_id = b.id
WHERE m.id = 1
ORDER BY br.borrowed_date DESC;


-- total copies per book
SELECT b.title, COUNT(*) AS total_copies
FROM books b
JOIN book_copies bc ON b.id = bc.book_id
GROUP BY b.title
ORDER BY b.title;


-- most borrowed books
SELECT b.title, COUNT(br.id) AS times_borrowed
FROM books b
JOIN book_copies bc ON b.id = bc.book_id
JOIN borrow_records br ON bc.id = br.book_copy_id
GROUP BY b.title
ORDER BY times_borrowed DESC;


-- borrowing count per member
SELECT m.full_name, COUNT(br.id) AS total_borrowed
FROM members m
JOIN borrow_records br ON m.id = br.member_id
GROUP BY m.full_name
ORDER BY total_borrowed DESC;
