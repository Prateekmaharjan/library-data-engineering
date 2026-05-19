import pandas as pd
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)
query= """
        select members.full_name, books.title, borrow_records.due_date, DATEDIFF(CURRENT_DATE, due_date) as days_overdue
from members 
inner join borrow_records on members.id=borrow_records.member_id 
inner join book_copies on book_copies.id=borrow_records.book_copy_id
inner join books on books.id=book_copies.book_id
where due_date<current_date and returned_date is null
"""
df=pd.read_sql(query, connection)

print(df)

df = df.rename(columns={
    'full_name': 'Member Name',
    'title': 'Book Title',
    'due_date': 'Due Date',
    'days_overdue': 'Days Overdue'
})

df['Severity'] = df['Days Overdue'].apply(lambda x: 'Critical' if x > 30 else 'Overdue')

import datetime
df['Report Generated'] = datetime.date.today()

try:
    df.to_csv('overdue_report.csv', index=False)
    print("Report saved to overdue_report.csv!")

except Exception as e:
    print("Failed to save report!", e)

connection.close()  