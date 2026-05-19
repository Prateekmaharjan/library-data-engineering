import pandas as pd
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

query = """
    SELECT members.full_name, books.title, borrow_records.borrowed_date
    FROM members
    INNER JOIN borrow_records ON members.id = borrow_records.member_id
    INNER JOIN book_copies ON book_copies.id = borrow_records.book_copy_id
    INNER JOIN books ON books.id = book_copies.book_id
    WHERE returned_date IS NULL
"""

df = pd.read_sql(query, connection)

print(df)

connection.close()