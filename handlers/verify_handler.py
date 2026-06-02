from services.auth_service import AuthService
from zalo_bot import Update

class VerifyHandler:
    def __init__(self, bot):
        self.bot = bot
        self.auth_service = AuthService()
    
    async def handle(self, update: Update, context, user_id: str, invite_key: str):
        chat_id = str(update.message.chat.id)
        result = await self.auth_service.verify_user(
            zalo_id = chat_id,
            user_id = user_id,
            invite_key = invite_key
        )
        await update.message.reply_text(result["message"])
        
