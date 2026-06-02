from zalo_bot import Update
from services.auth_service import AuthService

class AuthHandler:
    #Handler for /start command - show guide to user
    def __init__(self, bot):
        self.bot = bot
        self.auth_service = AuthService()
    
    async def handle(self, update: Update, context):
        # Check if user is already verified
        chat_id = str(update.message.chat.id)
        is_verified = await self.auth_service.is_user_verified(chat_id)
        
        if is_verified:
            await update.message.reply_text(
                "✅ Bạn đã xác minh rồi!\n"
                "Hãy gửi tin nhắn để chat với trợ lý ảo."
            )
        else:
            await update.message.reply_text(
                "Chào bạn! Tôi là trợ lý ảo của Hòa Phát Logistics.\n"
                "Để sử dụng dịch vụ, vui lòng xác minh tài khoản.\n"
                "📌Gửi: <mã nhân viên> <invite_key>\n"
                "Ví dụ: 001 abc123xyz"
                "\nLiên hệ admin nếu bạn chưa có mã xác thực."
            )
            