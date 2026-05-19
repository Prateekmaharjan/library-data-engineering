CREATE INDEX idx_books_title
ON books (title);

CREATE INDEX idx_members_email
ON members (email);

CREATE INDEX idx_book_copies_book_id
ON book_copies (book_id);

CREATE INDEX idx_borrow_records_member_id
ON borrow_records (member_id);

CREATE INDEX idx_borrow_records_book_copy_id
ON borrow_records (book_copy_id);

CREATE INDEX idx_borrow_records_due_date
ON borrow_records (due_date);
