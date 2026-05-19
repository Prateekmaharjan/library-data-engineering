from pyspark.sql import SparkSession
from pyspark.sql.functions import count, col, when, datediff, current_date

# Start Spark Session
spark = SparkSession.builder \
    .appName("LibraryAnalysis") \
    .config("spark.jars", "D:/library_management_db - ETL/mysql-connector-j-9.7.0/mysql-connector-j-9.7.0/mysql-connector-j-9.7.0.jar")\
    .getOrCreate()

print("Spark Session started!")

# Database connection properties
url = "jdbc:mysql://localhost:3306/library_db"
properties = {
    "user": "root",
    "password": "root123",
    "driver": "com.mysql.cj.jdbc.Driver"
}

# ============================================
# EXTRACT — Read tables from MySQL
# ============================================
print("Reading data from MySQL...")

members_df = spark.read.jdbc(url=url, table="members", properties=properties)
books_df = spark.read.jdbc(url=url, table="books", properties=properties)
borrow_df = spark.read.jdbc(url=url, table="borrow_records", properties=properties)
book_copies_df = spark.read.jdbc(url=url, table="book_copies", properties=properties)

print(f"Members: {members_df.count()}")
print(f"Books: {books_df.count()}")
print(f"Borrow Records: {borrow_df.count()}")

# ============================================
# ANALYSIS 1 — Most borrowed books
# ============================================
print("\n--- Most Borrowed Books ---")

most_borrowed = borrow_df \
    .join(book_copies_df, borrow_df.book_copy_id == book_copies_df.id) \
    .join(books_df, book_copies_df.book_id == books_df.id) \
    .groupBy(books_df.title) \
    .agg(count("*").alias("total_borrows")) \
    .orderBy(col("total_borrows").desc())

most_borrowed.show()

# ============================================
# ANALYSIS 2 — Overdue members
# ============================================
print("\n--- Overdue Members ---")

overdue = borrow_df \
    .filter(borrow_df.returned_date.isNull()) \
    .filter(borrow_df.due_date < current_date()) \
    .join(members_df, borrow_df.member_id == members_df.id) \
    .select(
        members_df.full_name,
        borrow_df.due_date,
        datediff(current_date(), borrow_df.due_date).alias("days_overdue")
    ) \
    .orderBy(col("days_overdue").desc())

overdue.show()

# ============================================
# ANALYSIS 3 — Member borrowing summary
# ============================================
print("\n--- Member Borrowing Summary ---")

member_summary = borrow_df \
    .join(members_df, borrow_df.member_id == members_df.id) \
    .groupBy(members_df.full_name) \
    .agg(
        count("*").alias("total_borrows"),
        count(when(borrow_df.returned_date.isNull(), 1)).alias("currently_borrowed")
    ) \
    .orderBy(col("total_borrows").desc())

member_summary.show()

spark.stop()
print("Analysis complete!")