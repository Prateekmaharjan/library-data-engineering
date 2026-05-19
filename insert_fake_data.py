import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

cursor = connection.cursor()

# ============================================
# INSERT FAKE AUTHORS
# ============================================
print("Inserting authors...")
author_ids = []
for _ in range(4):
    first_name = fake.first_name()
    last_name = fake.last_name()
    cursor.execute(
        "INSERT INTO authors (first_name, last_name) VALUES (%s, %s)",
        (first_name, last_name)
    )
    author_ids.append(cursor.lastrowid)
connection.commit()
print(f"Inserted {len(author_ids)} authors")

# ============================================
# INSERT FAKE BOOKS
# ============================================
print("Inserting books...")
book_ids = []
for _ in range(4):
    title = fake.catch_phrase()
    isbn = fake.isbn13()
    published_year = random.randint(1950, 2023)
    cursor.execute(
        "INSERT INTO books (title, isbn, published_year) VALUES (%s, %s, %s)",
        (title, isbn, published_year)
    )
    book_ids.append(cursor.lastrowid)
connection.commit()
print(f"Inserted {len(book_ids)} books")

# ============================================
# INSERT BOOK_AUTHORS (junction table)
# ============================================
print("Inserting book_authors...")
for book_id in book_ids:
    # Each book gets 1-2 random authors
    num_authors = random.randint(1, 2)
    selected_authors = random.sample(author_ids, num_authors)
    for author_id in selected_authors:
        cursor.execute(
            "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)",
            (book_id, author_id)
        )
connection.commit()
print("Inserted book_authors")

# ============================================
# INSERT BOOK COPIES
# ============================================
print("Inserting book copies...")
copy_ids = []
for book_id in book_ids:
    num_copies = random.randint(1, 3)
    for _ in range(num_copies):
        cursor.execute(
            "INSERT INTO book_copies (book_id, is_available) VALUES (%s, %s)",
            (book_id, 1)
        )
        copy_ids.append(cursor.lastrowid)
connection.commit()
print(f"Inserted {len(copy_ids)} book copies")

# ============================================
# INSERT FAKE MEMBERS
# ============================================
print("Inserting members...")
member_ids = []
for _ in range(50):
    full_name = fake.name()
    email = fake.email()
    phone = fake.numerify('98########')
    joined_date = fake.date_between(start_date=date(2023, 1, 1), end_date=date.today())
    cursor.execute(
        """INSERT INTO members (full_name, email, phone_number, joined_date) 
           VALUES (%s, %s, %s, %s)""",
        (full_name, email, phone, joined_date)
    )
    member_ids.append(cursor.lastrowid)
connection.commit()
print(f"Inserted {len(member_ids)} members")

# ============================================
# INSERT BORROW RECORDS
# ============================================
print("Inserting borrow records...")
borrow_count = 0
for member_id in member_ids:
    num_borrows = random.randint(2, 3)
    for _ in range(num_borrows):
        copy_id = random.choice(copy_ids)
        borrowed_date = fake.date_between(
            start_date=date(2024, 1, 1), 
            end_date=date.today()
        )
        due_date = borrowed_date + timedelta(days=14)
        
        # 60% chance book is returned
        if random.random() < 0.6:
            returned_date = borrowed_date + timedelta(days=random.randint(1, 20))
        else:
            returned_date = None
            
        cursor.execute(
            """INSERT INTO borrow_records 
               (member_id, book_copy_id, borrowed_date, due_date, returned_date) 
               VALUES (%s, %s, %s, %s, %s)""",
            (member_id, copy_id, borrowed_date, due_date, returned_date)
        )
        borrow_count += 1

connection.commit()
print(f"Inserted {borrow_count} borrow records")

cursor.close()
connection.close()
print("All fake data inserted successfully!")