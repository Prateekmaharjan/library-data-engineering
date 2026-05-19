ALTER TABLE book_authors
    ADD CONSTRAINT fk_book_authors_book
    FOREIGN KEY (book_id)
    REFERENCES books (id);

ALTER TABLE book_authors
    ADD CONSTRAINT fk_book_authors_author
    FOREIGN KEY (author_id)
    REFERENCES authors (id);

ALTER TABLE book_copies
    ADD CONSTRAINT fk_book_copies_book
    FOREIGN KEY (book_id)
    REFERENCES books (id);

ALTER TABLE borrow_records
    ADD CONSTRAINT fk_borrow_records_member
    FOREIGN KEY (member_id)
    REFERENCES members (id);

ALTER TABLE borrow_records
    ADD CONSTRAINT fk_borrow_records_book_copy
    FOREIGN KEY (book_copy_id)
    REFERENCES book_copies (id);

ALTER TABLE books
    ADD CONSTRAINT uq_books_isbn
    UNIQUE (isbn);