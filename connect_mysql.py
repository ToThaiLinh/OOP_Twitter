import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

try:
    # Kết nối đến MySQL
    db = mysql.connector.connect(
        host=host,        
        user=user,             
        password=password,  
        database=database  
    )

    # Kiểm tra kết nối
    if db.is_connected():
        print("Connected to MySQL server successfully.")
    else:
        print("Failed to connect to MySQL server.")

except Error as e:
    print(f"Error: {e}")

finally:
    if db.is_connected():
        db.close()


