DELIMITER $$

DROP PROCEDURE IF EXISTS borrow_book$$
CREATE PROCEDURE borrow_book(
    IN p_member_id BIGINT,
    IN p_book_copy_id BIGINT,
    IN p_due_date DATE
)
BEGIN
    INSERT INTO borrow_records (
        member_id,
        book_copy_id,
        due_date
    )
    VALUES (
        p_member_id,
        p_book_copy_id,
        p_due_date
    );

    UPDATE book_copies
    SET is_available = 0
    WHERE id = p_book_copy_id;
END$$


DROP PROCEDURE IF EXISTS return_book$$
CREATE PROCEDURE return_book(
    IN p_book_copy_id BIGINT
)
BEGIN
    UPDATE borrow_records
    SET returned_date = CURRENT_DATE
    WHERE book_copy_id = p_book_copy_id
      AND returned_date IS NULL;

    UPDATE book_copies
    SET is_available = 1
    WHERE id = p_book_copy_id;
END$$

DELIMITER ;