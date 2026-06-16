import mysql.connector

class Database:
    def __init__(self, dictionary: bool = False):
        self.conn = None
        self.cursor = None
        self.dictionary = dictionary

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='logistics_db',
                charset='utf8mb4'
            )
            self.cursor = self.conn.cursor(dictionary=self.dictionary)
            print("Connected to database!")
            return self
        except Exception as e:
            print(f"Connection error: {e}")
            raise e

    def upsert_many(self, sql: str, batch: list[tuple]) -> int:
        # Nothing to write when the prepared batch is empty.
        if not batch:
            return 0
        try:
            # Execute the same INSERT ... ON DUPLICATE KEY UPDATE statement for all rows.
            self.cursor.executemany(sql, batch)
            # Commit only after the full batch succeeds.
            self.conn.commit()
            return self.cursor.rowcount
        except Exception:
            # Roll back the whole batch so MySQL does not keep partial updates.
            if self.conn:
                self.conn.rollback()
            raise
        
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed!")
            
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
