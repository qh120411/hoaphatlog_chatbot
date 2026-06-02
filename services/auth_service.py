from database.db_connect import Database

class AuthService:
    def __init__(self):
        self.db = Database()
        
    async def verify_user(self, zalo_id: str, user_id : str, invite_key: str) -> dict:
        if not user_id or not invite_key:
            return {
                "success": False,
                "message": "Sai mã xác thực, vui lòng thử lại."
            }
        try:
            with self.db as db:
                # Lần 1 verify: zalo_id IS NULL
                sql = """
                    UPDATE chat_user
                    SET zalo_id = %s, status = 'active', updated_at = NOW()
                    WHERE user_id = %s AND invite_key = %s AND zalo_id IS NULL
                    LIMIT 1
                """
                db.cursor.execute(sql, (zalo_id, user_id, invite_key))
                db.conn.commit()
            
                if db.cursor.rowcount == 1:
                    print(f"✅ User {user_id} verified with zalo_id {zalo_id}")
                    return {
                        "success": True,
                        "message": "Xác minh thành công! Bạn đã có thể sử dụng dịch vụ."
                    }
                
                # Lần 2+: Check zalo_id có match không
                sql_check = """
                    SELECT 1 FROM chat_user
                    WHERE user_id = %s AND invite_key = %s AND zalo_id = %s AND status = 'active'
                    LIMIT 1
                """
                db.cursor.execute(sql_check, (user_id, invite_key, zalo_id))
                
                if db.cursor.fetchone():
                    return {
                        "success": True,
                        "message": "Bạn đã xác minh rồi!"
                    }
                
                # Lần 2+ nhưng zalo_id khác
                return {
                    "success": False,
                    "message": "Mã xác thực không hợp lệ hoặc đã được dùng bởi người khác."
                }
            
        except Exception as e:
            print(f"❌ Error verifying user {user_id}: {e}")
            return {
                "success": False,
                "message": "Lỗi hệ thống, vui lòng thử lại sau."
            }
    
    async def is_user_verified(self, zalo_id: str) -> bool:
        try:
            with self.db as db:
                sql = """
                    SELECT 1
                    FROM chat_user
                    WHERE zalo_id = %s AND status = 'active'
                    LIMIT 1
                """
                db.cursor.execute(sql, (zalo_id,))
                result = db.cursor.fetchone()
                
                is_verified = result is not None
                print(f"User with zalo_id {zalo_id} verification status: {is_verified}")
                return is_verified
        except Exception as e:
            print(f"❌ Error checking verification for zalo_id {zalo_id}: {e}")
            return False
                
