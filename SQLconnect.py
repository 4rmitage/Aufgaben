import mysql.connector

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456m,",
)

print(my_db)