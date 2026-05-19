''' The library manager wants a monthly summary report. Create an ETL pipeline that extracts all members and their total number of books borrowed,
transforms the data by adding a membership status column that says 'Active Borrower' if they have borrowed at least one book and 'Inactive'
if they have never borrowed, and loads the result into a CSV called member_summary.csv.'''

import pandas as pd
import mysql.connector 
import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="library_db"
    )

def extract(connection):
    print("Extracting data from database")
    query=""" select members.full_name,
      count(borrow_records.book_copy_id) as total_borrows
      from members 
      left join borrow_records on members.id=borrow_records.member_id
      left join book_copies on book_copies.id=borrow_records.book_copy_id
      left join books on books.id=book_copies.book_id
      GROUP BY members.id, members.full_name
    """
    df=pd.read_sql (query, connection)
    print(f"Extracted {len(df)} records")
    return df 

def transform(df):
    print("Transforming Data")

    df= df.rename(columns={
        'full_name': 'Member Name',
        'total_borrows': 'Total Books Borrowed'})
    
    df['Membership Status']= df['Total Books Borrowed'].apply(
    lambda x:'Active Borrower' if x>0 else 'Inactive')

    today = datetime.date.today()
    df['Report Generated'] = today
    return df

def load(df):
    print("Loading Data..")
    try:
        df.to_csv('member_summary.csv', index=False)
        print("Saved CSV file to member_summary.csv ")
    except Exception as e:
        print("Failed to save data!", e)


connection= get_connection()
extracted = extract(connection)
df_transformed=transform(extracted)
print(df_transformed)
load(df_transformed)