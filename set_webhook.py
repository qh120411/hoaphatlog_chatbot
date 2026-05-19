from zalo_bot import Bot

TOKEN = "746472850277050914:IEUgaCtPOrvqrRQwPJUAJpDvlxTSXLkOlxfocWDBFSPunWBflBRrxHOhvUJvQUdq"
WEBHOOK_URL = "https://grew-unending-ageless.ngrok-free.dev/webhook"

bot = Bot(token=TOKEN)

result = bot.set_webhook(url=WEBHOOK_URL)

print(result)