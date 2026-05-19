import pandas as pd
import mysql.connector
import datetime

# ============================================
# DATABASE CONNECTION
# ============================================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="library_db"
    )

# ============================================
# EXTRACT
# ============================================
def extract(connection):
    print("Extracting data...")
    query = """
        SELECT 
            members.full_name,
            books.title,
            borrow_records.borrowed_date,
            borrow_records.due_date,
            borrow_records.returned_date
        FROM members
        INNER JOIN borrow_records ON members.id = borrow_records.member_id
        INNER JOIN book_copies ON book_copies.id = borrow_records.book_copy_id
        INNER JOIN books ON books.id = book_copies.book_id
    """
    df = pd.read_sql(query, connection)
    print(f"Extracted {len(df)} records")
    return df


# ============================================
# TRANSFORM
# ============================================
def transform(df):
    print("Transforming data...")

    # Rename columns
    df = df.rename(columns={
        'full_name': 'Member Name',
        'title': 'Book Title',
        'borrowed_date': 'Borrowed Date',
        'due_date': 'Due Date',
        'returned_date': 'Returned Date'
    })

   # Add status column
    df['Status'] = df['Returned Date'].apply(
    lambda x: 'Returned' if pd.notna(x) else 'Not Returned'
)

    # Add days overdue column
    today = datetime.date.today()
    df['Days Overdue'] = df.apply(
    lambda row: (today - row['Due Date']).days
    if row['Returned Date'] is None and pd.notna(row['Due Date']) and row['Due Date'] < today
    else 0, axis=1
)

    # Add report generated date
    df['Report Generated'] = today

    print(f"Transformation complete — {len(df)} records processed")
    return df

# ============================================
# LOAD
# ============================================
def load(df):
    print("Loading data...")
    try:
        df.to_csv('library_etl_report.csv', index=False)
        print("Data successfully saved to library_etl_report.csv!")
    except Exception as e:
        print("Failed to save data!", e)

# ============================================
# MAIN — runs everything
# ============================================
connection = get_connection()
df_raw = extract(connection)
df_transformed = transform(df_raw)
load(df_transformed)
connection.close()