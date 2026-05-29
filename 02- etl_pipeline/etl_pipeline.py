import pandas as pd
import mysql.connector
import datetime

# DATABASE CONNECTION
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="library_db"
    )

# EXTRACT
def extract_most_borrowed_books(connection):
    print("Extracting most borrowed books data...")
    query = """
        SELECT 
            books.title AS book_title,
            CONCAT(authors.first_name, ' ', authors.last_name) AS author,
            COUNT(borrow_records.id) AS total_borrows,
            SUM(CASE WHEN borrow_records.returned_date IS NULL 
                THEN 1 ELSE 0 END) AS currently_borrowed
        FROM books
        INNER JOIN book_copies ON book_copies.book_id = books.id
        INNER JOIN borrow_records ON borrow_records.book_copy_id = book_copies.id
        INNER JOIN book_authors ON book_authors.book_id = books.id
        INNER JOIN authors ON authors.id = book_authors.author_id
        GROUP BY books.id, books.title, authors.first_name, authors.last_name
        ORDER BY total_borrows DESC
    """
    df = pd.read_sql(query, connection)
    print(f"Extracted {len(df)} books")
    return df

def extract_member_activity(connection):
    print("Extracting member activity data...")
    query = """
        SELECT
            members.full_name AS member_name,
            COUNT(borrow_records.id) AS total_borrows,
            SUM(CASE WHEN borrow_records.returned_date IS NOT NULL 
                THEN 1 ELSE 0 END) AS total_returned,
            SUM(CASE WHEN borrow_records.returned_date IS NULL 
                THEN 1 ELSE 0 END) AS currently_holding,
            SUM(CASE WHEN borrow_records.returned_date IS NULL 
                AND borrow_records.due_date < CURDATE() 
                THEN 1 ELSE 0 END) AS overdue_count
        FROM members
        INNER JOIN borrow_records ON borrow_records.member_id = members.id
        GROUP BY members.id, members.full_name
        ORDER BY total_borrows DESC
    """
    df = pd.read_sql(query, connection)
    print(f"Extracted {len(df)} members")
    return df

def extract_overdue_analysis(connection):
    print("Extracting overdue analysis data...")
    query = """
        SELECT
            members.full_name AS member_name,
            books.title AS book_title,
            borrow_records.borrowed_date,
            borrow_records.due_date,
            DATEDIFF(CURDATE(), borrow_records.due_date) AS days_overdue,
            CASE
                WHEN DATEDIFF(CURDATE(), borrow_records.due_date) <= 7 THEN 'Low'
                WHEN DATEDIFF(CURDATE(), borrow_records.due_date) <= 30 THEN 'Medium'
                ELSE 'High'
            END AS severity
        FROM borrow_records
        INNER JOIN members ON members.id = borrow_records.member_id
        INNER JOIN book_copies ON book_copies.id = borrow_records.book_copy_id
        INNER JOIN books ON books.id = book_copies.book_id
        WHERE borrow_records.returned_date IS NULL
        AND borrow_records.due_date < CURDATE()
        ORDER BY days_overdue DESC
    """
    df = pd.read_sql(query, connection)
    print(f"Extracted {len(df)} overdue records")
    return df

# TRANSFORM
def transform_most_borrowed_books(df):
    print("Transforming most borrowed books data...")
    df['report_generated'] = datetime.date.today()
    print(f"Transformation complete — {len(df)} books processed")
    return df

def transform_member_activity(df):
    print("Transforming member activity data...")
    df['report_generated'] = datetime.date.today()
    # Classify members by activity level based on total borrows
    df['activity_level'] = df['total_borrows'].apply(
        lambda x: 'High' if x >= 10 else ('Medium' if x >= 5 else 'Low')
    )
    print(f"Transformation complete — {len(df)} members processed")
    return df

def transform_overdue_analysis(df):
    print("Transforming overdue analysis data...")
    df['report_generated'] = datetime.date.today()
    print(f"Transformation complete — {len(df)} overdue records processed")
    return df

# LOAD
def load(df, filename, report_name):
    print(f"Loading {report_name}...")
    try:
        df.to_csv(filename, index=False)
        print(f"Successfully saved {filename} — {len(df)} records")
    except Exception as e:
        print(f"Failed to save {filename}", e)

# MAIN
print("=" * 50)
print("Library Management ETL Pipeline Starting...")
print("=" * 50)

connection = get_connection()

df_books_raw = extract_most_borrowed_books(connection)
df_books = transform_most_borrowed_books(df_books_raw)
load(df_books, 'report_most_borrowed_books.csv', 'Most Borrowed Books Report')

df_members_raw = extract_member_activity(connection)
df_members = transform_member_activity(df_members_raw)
load(df_members, 'report_member_activity.csv', 'Member Activity Report')

df_overdue_raw = extract_overdue_analysis(connection)
df_overdue = transform_overdue_analysis(df_overdue_raw)
load(df_overdue, 'report_overdue_analysis.csv', 'Overdue Analysis Report')

connection.close()

print("=" * 50)
print("ETL Pipeline Complete — 3 reports generated")
print("=" * 50)