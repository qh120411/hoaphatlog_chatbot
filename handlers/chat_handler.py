import asyncio
from services.auth_service import AuthService
from AI.chat_orchestrator import ChatOrchestrator
from zalo_bot import Update
from zalo_bot.constants import ChatAction

class ChatHandler:
    def __init__(self, bot):
        self.bot = bot
        self.auth_service = AuthService()
        self.chat_orchestrator = ChatOrchestrator()
    
    async def show_typing(self, chat_id: str):
        await self.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )
    
    async def handle(self, update: Update, context):
        #check if user is verified
        chat_id = str(update.message.chat.id)
        user_text = update.message.text
        
        try:
            is_verified = await self.auth_service.is_user_verified(chat_id)
            
            if not is_verified:
                await update.message.reply_text(
                    "❌ Bạn không còn quyền sử dụng dịch vụ!\n"
                    "Liên hệ quản lý nếu có thắc mắc."
                )
                print(f"⚠️ Unverified user {chat_id}")
                return
            print(f"💬 Chat from {chat_id}: {user_text}")
            await self.show_typing(chat_id)
            await asyncio.sleep(1)
            
            response = await self.chat_orchestrator.handle(user_text)
            await update.message.reply_text(response)
            print(f"✅Replied to {chat_id}")
            
        except Exception as e:
            print(f"❌ Chat error: {e}")
            try:
                await update.message.reply_text("❌ Lỗi, vui lòng thử lại.")
            except:
                pass
