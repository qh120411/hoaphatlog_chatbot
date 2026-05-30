from fastapi import FastAPI
from zalo.sender import app
from zalo.set_webhook import ZaloWebhook
from config.config import Config

if __name__ == "__main__":
    print("Setting up Zalo webhook...")
    try:
        webhook = ZaloWebhook()
        webhook.set_webhook()
    except Exception as e:
        print(f"Warning: Could not set webhook: {e}")
        print("Make sure WEBHOOK_URL in .env is correct")
    print("Starting bot...\n")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)