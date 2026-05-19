''' Write a Python script that asks the user to enter a member id and then fetches and prints that 
specific member's details from the database.'''

import mysql.connector 

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="library_db"
)

cursor=connection.cursor()

member_id= input("Enter member_id: ")

cursor.execute("select * from members where id = %s", (member_id,))

result=cursor.fetchall()

print ("the members details are", result)