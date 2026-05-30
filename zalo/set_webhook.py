from config.config import Config
from zalo_bot import Bot
import secrets

class ZaloWebhook:
    def __init__(self):
        self.bot = Bot(token=Config.ZALO_TOKEN)
        self.webhook_url = Config.WEBHOOK_URL
        self.secret_token = secrets.token_urlsafe(32)
    
    def set_webhook(self):
        try:
            res = self.bot.set_webhook(self.webhook_url, self.secret_token)
            if res:  # True nếu thành công
                print("✅ Webhook set successfully!")
                print(f"   URL: {self.webhook_url}")
                print(f"   Secret Token: {self.secret_token}")
            else:
                print(f"❌ Failed to set webhook")
        except Exception as e:
            print(f"❌ Error setting webhook: {e}")

