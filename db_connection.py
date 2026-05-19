## mysql
''' import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

if connection.is_connected():
    print("Successfully connected to the database!")
    connection.close()
    '''

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM members")

results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
connection.close()