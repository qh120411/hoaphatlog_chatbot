import re
from src.user_store import verify_user, get_user, is_verified

ROLE_PATTERNS = {
    "admin"     : r"^AD\d{3,5}$",
    "quan_ly"   : r"^QL\d{3,5}$",
    "nhan_vien" : r"^NV\d{3,5}$",
}

def detec_role(ma_user: str) -> str | None:
    ma_user = ma_user.strip().upper()
    for role, pattern in ROLE_PATTERNS.items():
        if re.match(pattern, ma_user):
            return role
    return None

def authenticate_user(telegram_id: int, ma_user: str, ho_ten: str) -> dict:
    
    ma_user = ma_user.strip().upper()
    role = detec_role(ma_user)
    if not role:
        return {
            "success": False,
            "role": None,
            "message": ( "Mã nhân viên không hợp lệ. Vui lòng kiểm tra lại." )
        }
        
    success = verify_user(telegram_id = telegram_id, ma_user = ma_user, role = role)
    if not success:
        return {
            "success": False,
            "role": None,
            "message": ( "Xác minh thất bại. Vui lòng kiểm tra lại hoặc liên hệ với quản lý/ admin ." )
        }
    role_label = {
        "admin": "Admin",
        "quan_ly": "Quản lý",
        "nhan_vien": "Nhân viên"
    }
    return {
        "success" : True,
        "role" : role,
        "message" : (
            f"Xin chào {ho_ten}! Bạn đã được xác minh thành công với vai trò {role_label.get(role)}.\n"
            f"Gõ /help để xem cách hướng dẫn dùng nhé!"
        )
    }

def check_permission(telegram_id: int, required_role: str) -> bool:
    user = get_user(telegram_id)
    if not user or not user.get("is_verified"):
        return False
    role_level = {
        "admin": 3,
        "quan_ly": 2,
        "nhan_vien": 1
    }
    user_level = role_level.get(user.get("role"), 0)
    required_level = role_level.get(required_role, 99)
    
    return user_level >= required_level
    
    