import mysql.connector

db = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "crud"
}

def get_db_connection():
    return mysql.connector.connect(**db)