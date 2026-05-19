CREATE DATABASE library_dw;
USE library_dw;

-- Dimension table for members
CREATE TABLE dim_member (
    member_id BIGINT NOT NULL,
    member_name VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    phone_number VARCHAR(20),
    joined_date DATE,
    PRIMARY KEY (member_id)
);

-- Dimension table for books
CREATE TABLE dim_book (
    book_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    author_name VARCHAR(200),
    published_year INT,
    PRIMARY KEY (book_id)
);

-- Dimension table for dates
CREATE TABLE dim_date (
    date_id BIGINT NOT NULL AUTO_INCREMENT,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    quarter INT,
    year INT,
    day_of_week VARCHAR(20),
    PRIMARY KEY (date_id)
);

-- Fact table
CREATE TABLE fact_borrow (
    borrow_id BIGINT NOT NULL AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    book_id BIGINT NOT NULL,
    date_id BIGINT NOT NULL,
    days_borrowed INT,
    is_returned TINYINT,
    is_overdue TINYINT,
    PRIMARY KEY (borrow_id),
    FOREIGN KEY (member_id) REFERENCES dim_member(member_id),
    FOREIGN KEY (book_id) REFERENCES dim_book(book_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);