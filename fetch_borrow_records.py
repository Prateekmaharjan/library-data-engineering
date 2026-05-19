'''Write a Python script that fetches all borrow records where the book has not been returned yet and
displays member name, book title and borrowed date.'''

import mysql.connector 

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

cursor =connection.cursor()

cursor.execute("""
               select members.full_name, books.title, borrow_records.borrowed_date 
               from members
               inner join borrow_records on members.id=borrow_records.member_id
               inner join book_copies on book_copies.id=borrow_records.book_copy_id
               inner join books on books.id=book_copies.book_id
               where returned_date is null""")

results=cursor.fetchall()

for row in results: 
    print (row)

cursor.close()
connection.close()