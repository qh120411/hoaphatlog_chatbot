from zalo.sender import app
from zalo.set_webhook import ZaloWebhook
from sync_data import sync_data
import asyncio
import logging

async def sync_loop():
    while True:
        try:
            await asyncio.to_thread(sync_data)
            print("✅ All data synced successfully. Next sync in 5 min.")
        except Exception as e:
            logging.exception(f"Sync data failed: {e}")

        await asyncio.sleep(300)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(sync_loop())

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