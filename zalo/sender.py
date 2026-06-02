import re
from fastapi import FastAPI, Request
from config.config import Config
from zalo_bot import Bot, Update
from handlers.auth_handler import AuthHandler
from handlers.verify_handler import VerifyHandler
from handlers.chat_handler import ChatHandler
from services.auth_service import AuthService

app = FastAPI()

VERIFY_COMMAND = "/start"
USER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
INVITE_KEY_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")

class MockContext:
    def __init__(self, bot):
        self.bot = bot


class ZaloBotManager:
    # Routes Zalo messages to appropriate handlers based on user state
    
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.auth_handler = AuthHandler(self.bot)
        self.verify_handler = VerifyHandler(self.bot)
        self.chat_handler = ChatHandler(self.bot)
        self.auth_service = AuthService()
    
    def is_verify_format(self, text: str) -> tuple:
        if not text:
            return False, None, None

        parts = text.strip().split()
        if len(parts) != 2:
            return False, None, None

        user_id, invite_key = parts
        if not USER_ID_PATTERN.fullmatch(user_id):
            return False, None, None
        if not INVITE_KEY_PATTERN.fullmatch(invite_key):
            return False, None, None

        return True, user_id, invite_key
    
    async def handle_update(self, update: Update):
        context = MockContext(self.bot)
        if not update.message:
            print("⚠️ Update with no message received, ignoring.")
            return
        
        text = update.message.text
        chat_id = str(update.message.chat.id)
        
        # Step 1: /start command
        if text == VERIFY_COMMAND:
            print("📌 /start command received")
            await self.auth_handler.handle(update, context)
            return
        
        # Step 2: Check verification status
        is_verified = await self.auth_service.is_user_verified(chat_id)
        
        # Step 3: Verified users → always chat
        if is_verified:
            print(f"💬 Chat message from verified user {chat_id}")
            await self.chat_handler.handle(update, context)
            return
        
        # Step 4: Unverified users - check verify format
        if self.is_verify_format(text)[0]:
            _, user_id, invite_key = self.is_verify_format(text)
            print(f"🔐 Verification attempt: user_id={user_id}")
            await self.verify_handler.handle(update, context, user_id, invite_key)
        else:
            # Step 5: Not verified + wrong format → chat_handler rejects
            print(f"💬 Chat message from unverified user {chat_id}")
            await self.chat_handler.handle(update, context)


zalo_bot = ZaloBotManager(token=Config.ZALO_TOKEN)

@app.post("/webhook/zalo")
async def zalo_webhook(request: Request):
    try:
        data = await request.json()
        print(f"📥 Received webhook: {data}")
        
        event_data = data.get("result", data)
        update = Update.de_json(event_data, zalo_bot.bot)
        
        print(f"📝 Update object: {update}")
        if update.message:
            print(f"👤 Chat ID: {update.message.chat.id}")
            print(f"💬 Text: {update.message.text}")
        
        await zalo_bot.handle_update(update)
        print("✅ Response sent successfully")
        return {"ok": True}

    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return {"ok": False, "error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "ok"}