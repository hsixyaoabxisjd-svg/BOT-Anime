from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from app.workers.tasks import process_video_task

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! أرسل رابط فيديو أو ملف فيديو أو اسم أنمي/حلقة.\n"
        "أمثلة:\n"
        "- https://youtu.be/...\n"
        "- One Piece 1085\n"
        "- ملف mp4"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("أرسل رابطًا أو اسمًا أو ملفًا.")
        return

    if "http://" in text or "https://" in text:
        await update.message.reply_text("تم استلام الرابط. جاري تجهيز المهمة...")
        task = process_video_task.delay(update.effective_user.id, text, "url")
        await update.message.reply_text(f"تمت إضافة المهمة بنجاح.\nTask ID: {task.id}")
        return

    await update.message.reply_text(
        f"تم تسجيل طلب البحث: {text}\n"
        "سيتم البحث عن الحلقة/الفيلم المناسب لاحقًا."
    )

async def handle_video_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video
    if not file:
        await update.message.reply_text("لم يتم العثور على ملف فيديو.")
        return

    await update.message.reply_text("تم استلام الملف. جاري تجهيز المهمة...")
    task = process_video_task.delay(update.effective_user.id, file.file_id, "file")
    await update.message.reply_text(f"تمت إضافة المهمة.\nTask ID: {task.id}")


def build_application(bot_token: str):
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video_file))
    return app
