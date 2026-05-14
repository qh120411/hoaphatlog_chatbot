import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host = os.getenv("DB_HOST", "localhost"),
            port = int(os.getenv("DB_PORT", 3306)),
            user = os.getenv("DB_USER", "root"),
            password = os.getenv("DB_PASSWORD", ""),
            database = os.getenv("DB_NAME", "logistics"),
            charset = "utf8mb4",
        )
        return conn
    except Error as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None

def test():
    conn = get_connection()
    if conn and conn.is_connected():
        print("Kết nối cơ sở dữ liệu thành công!")
        conn.close()
    else:
        print("Kết nối cơ sở dữ liệu thất bại.")
    
if __name__ == "__main__":
    test()