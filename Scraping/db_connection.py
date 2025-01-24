# import os
# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv

# load_dotenv()

# def create_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host=os.getenv("DB_HOST"),
#             user=os.getenv("DB_USER"),
#             passwd=os.getenv("DB_PASS"),
#             database=os.getenv("DB_NAME")
#         )
#         print("MySQL Database connection successful")
#         return connection
#     except Error as e:
#         print(f"The error '{e}' occurred")
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def create_db_connection():
    try:
        
    # Print environment variables to verify they are loaded correctly
        print("DB_HOST:", os.getenv("DB_HOST"))
        print("DB_USER:", os.getenv("DB_USER"))
        print("DB_PASS:", os.getenv("DB_PASS"))
        print("DB_NAME:", os.getenv("DB_NAME"))
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("MySQL Database connection successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
