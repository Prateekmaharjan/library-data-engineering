from sqlalchemy import create_engine, text
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Source database
source_engine = create_engine(f"mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@172.18.240.1/library_db")

# Destination database
dest_engine = create_engine(f"mysql+mysqlconnector://root:{os.environ.get('DB_PASSWORD')}@172.18.240.1/library_dw")

print("Connected to both databases!")


def extract_and_load_dim_member():
    print("Loading dim_member...")
    
    # Truncate first 
    with dest_engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE dim_member"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    # Extract from source
    query = """
        SELECT id as member_id, full_name as member_name, email, 
        phone_number, joined_date
        FROM members
    """
    df = pd.read_sql(query, source_engine)
    
    # Load to warehouse
    df.to_sql('dim_member', dest_engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} members into dim_member")

"""
SNOWFLAKE SCHEMA ETL (Commented Out)
============================================

def extract_and_load_dim_author():
    print("Loading dim_author...")
    with dest_engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE dim_author"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    query = '''
        SELECT DISTINCT
            authors.id as author_id,
            CONCAT(authors.first_name, ' ', authors.last_name) as author_name
        FROM authors
    '''
    df = pd.read_sql(query, source_engine)
    df.to_sql('dim_author', dest_engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} authors into dim_author")

    def extract_and_load_dim_book_snowflake():
    print("Loading dim_book snowflake...")
    with dest_engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE dim_book"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    query = '''
        SELECT DISTINCT
            books.id as book_id,
            books.title,
            authors.id as author_id,
            books.published_year
        FROM books
        INNER JOIN book_authors ON books.id = book_authors.book_id
        INNER JOIN authors ON book_authors.author_id = authors.id
    '''
    df = pd.read_sql(query, source_engine)
    df.to_sql('dim_book', dest_engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} books into dim_book")
"""

def extract_and_load_dim_book ():
    print("Loading dim_books..")

    with dest_engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE dim_book"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    query=""" SELECT 
        books.id as book_id,
        books.title,
        GROUP_CONCAT(authors.first_name, ' ', authors.last_name) as author_name,
        books.published_year
        FROM books
        inner join book_authors on books.id=book_authors.book_id
        inner join authors on book_authors.author_id=authors.id 
        GROUP BY books.id, books.title, books.published_year
        """
    
    df=pd.read_sql(query, source_engine)
    df.to_sql('dim_book', dest_engine, if_exists='append', index=False)
    print(f"loaded {len(df)} members to the dim_books" )
    
def load_dim_date():
    print("Loading dim_date...")
    
    with dest_engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE dim_date"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    # Generate dates from 2024-01-01 to 2026-12-31
    dates = pd.date_range(start='2024-01-01', end='2026-12-31')
    
    df = pd.DataFrame({
        'full_date': dates,
        'day': dates.day,
        'month': dates.month,
        'quarter': dates.quarter,
        'year': dates.year,
        'day_of_week': dates.day_name()
    })
    
    df.to_sql('dim_date', dest_engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} dates into dim_date")

def extract_and_load_fact_borrow ():
    print("Loading dact_borrow table..")

    with dest_engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_borrow"))
        conn.commit()

    query=""" select 
        borrow_records.id as borrow_id,
        borrow_records.member_id,
        books.id as book_id,
        borrow_records.borrowed_date,
        CASE WHEN returned_date IS NOT NULL THEN DATEDIFF(returned_date, borrowed_date) ELSE 0 END as days_borrowed,
        CASE WHEN returned_date is NOT NULL THEN 1 ELSE 0 END as is_returned,
        CASE WHEN  due_date<current_date AND returned_date is NULL THEN 1 ELSE 0 END as is_overdue
        from borrow_records
        inner join book_copies on book_copies.id=borrow_records.book_copy_id
        inner join books on books.id=book_copies.book_id  """

    df = pd.read_sql(query, source_engine)
    
    # Get dim_date from warehouse
    dim_date_df = pd.read_sql("SELECT date_id, full_date FROM dim_date", dest_engine)
    
    # Merge to get date_id
    df = df.merge(dim_date_df, left_on='borrowed_date', right_on='full_date', how='left')
    
    # Drop columns not needed in fact table
    df = df.drop(columns=['borrowed_date', 'full_date'])
    
    # Load to warehouse
    df.to_sql('fact_borrow', dest_engine, if_exists='append', index=False)
    print(f"Loaded {len(df)} records into fact_borrow")

extract_and_load_dim_member()

# ---- Star Schema ----
extract_and_load_dim_book()
load_dim_date()
extract_and_load_fact_borrow()

"""
---- Snowflake Schema (commented out) ----
extract_and_load_dim_author()       # must run before dim_book
extract_and_load_dim_book_snowflake()
load_dim_date()
extract_and_load_fact_borrow()
"""