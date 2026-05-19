from flask import Flask, request
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, CommandHandler, MessageHandler, filters

TOKEN = "746472850277050914:IEUgaCtPOrvqrRQwPJUAJpDvlxTSXLkOlxfocWDBFSPunWBflBRrxHOhvUJvQUdq"

bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=0)


def start(update: Update, context):
    update.message.reply_text(
        f"Xin chào {update.effective_user.display_name}!"
    )


async def chat(update: Update, context):
    user_text = update.message.text
    print("USER:", user_text)
    await update.message.reply_text(f"Bạn vừa nói: {user_text}")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("EVENT:", data)

    update = Update.de_json(data, bot)
    dispatcher.process_update(update)

    return "ok"


@app.route("/", methods=["GET"])
def home():
    return "Bot webhook is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)