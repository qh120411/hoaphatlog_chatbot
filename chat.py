import os
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_FILE = 'users.json'

def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    if os.path.getsize(USER_FILE) == 0:
        return {}

    try:
        with open(USER_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    
    if not context.args:
        await update.message.reply_text(
            "Xin chào! Tôi là bot thông báo tự động của công ty Hòa Phát.\n\n"
            "Vui lòng gửi lệnh /start kèm theo mã nhân viên để đăng ký nhận thông báo.\n\n"
            "Ví dụ: /start NV001"
        )
        return
        
    employee_id = context.args[0].upper()
    users = load_users()
    
    users[employee_id]= {
        "employee_id": employee_id,
        "telegram_id": user.id,
        "chat_id": chat.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name
    }
    
    save_users(users)
    
    await update.message.reply_text(
        "Đã lưu thông tin của bạn ✅\n"
        f"full_name: {user.full_name}\n"
        f"user_id: {user.id}\n"
        f"chat_id: {chat.id}"
    )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Các lệnh có sẵn:\n"
        "/start - Đăng ký và bắt đầu sử dụng chatbot\n"
        "/help - Hiển thị hướng dẫn sử dụng"
    )
    
def main():
    if not TOKEN:
        print("Lỗi: Chưa có TELEGRAM_BOT_TOKEN trong biến môi trường.")
        return
    
    chat = ApplicationBuilder().token(TOKEN).build()
    chat.add_handler(CommandHandler("start", start))
    chat.add_handler(CommandHandler("help", help_command))
    
    print("Bot đang chạy...")
    chat.run_polling()
    
if __name__ == '__main__':
    main()