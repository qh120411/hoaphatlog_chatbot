from src.db import get_connection

def add_user(telegram_id: int, ho_ten: str) -> bool:
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (telegram_id, ho_ten) VALUES (%s, %s)", (telegram_id, ho_ten))
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi khi thêm người dùng: {e}")
        return False
    finally:
        conn.close()
        
def get_user(telegram_id: int):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Lỗi khi lấy người dùng: {e}")
        return None
    finally:
        conn.close()

def verify_user(telegram_id: int, ma_user: str, role: str) -> bool:
    conn = get_connection()
    if not conn: 
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET ma_user = %s, role = %s, is_verified = 1
            WHERE telegram_id = %s
            """,(ma_user, role, telegram_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Lỗi khi xác minh người dùng: {e}")
        return False
    finally:
        conn.close()
    
def is_verified(telegram_id: int) -> bool:
    user = get_user(telegram_id)
    if not user:
        return False
    return bool(user.get("is_verified"))
    
