import mysql.connector

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='logistics_db',
                charset='utf8mb4'
            )
            self.cursor = self.conn.cursor()
            print("✅ Connected to database!")
            return self
        except Exception as e:
            print(f"❌ Connection error: {e}")
            raise e
            
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("✅ Connection closed!")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        