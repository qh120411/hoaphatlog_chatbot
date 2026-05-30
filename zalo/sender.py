import asyncio

from fastapi import FastAPI, Request
from config.config import Config
from zalo_bot import Bot, Update
from zalo_bot.ext import ContextTypes
from zalo_bot.constants import ChatAction
from AI.router_client import LLM_Router

app = FastAPI()
class MockContext:
    #fake context
    def __init__(self, bot):
        self.bot = bot

class ZaloBotManager:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.llm_router = LLM_Router() 

    async def show_typing(self, chat_id: str):
        await self.bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat.id
        await self.show_typing(chat_id)
        await asyncio.sleep(2)
        await update.message.reply_text(
            "Xin chào! Tôi là trợ lý ảo của công ty Hòa Phát Logistics. "
            "Hãy gửi tin nhắn cho tôi để bắt đầu nhé!"
        )
        
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat.id
        user_text = update.message.text
        await self.show_typing(chat_id)
        await asyncio.sleep(1)
        response = await self.llm_router.call_llm(user_text)
        await update.message.reply_text(response)

    async def handle_update(self, update: Update):
        context = MockContext(self.bot)
        if not update.message:
            print("⚠️ Update không có message")
            return
        text = update.message.text
        
        if text == "/start":
            await self.start(update, context)
        else:
            await self.echo(update, context)

zalo_bot = ZaloBotManager(token=Config.ZALO_TOKEN)

@app.post("/webhook/zalo")
async def zalo_webhook(request: Request):
    try:
        data = await request.json()
        print(f"📥 Received data: {data}")
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