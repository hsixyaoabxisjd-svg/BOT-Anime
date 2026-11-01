import asyncio
from app.config import BOT_TOKEN
from app.bot.handlers import build_application

if __name__ == "__main__":
    print("Starting Telegram AI Dubbing Bot...")
    app = build_application(BOT_TOKEN)
    app.run_polling()
