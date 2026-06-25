from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI
from config import *
from memory import *

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Advanced Grok AI Bot\n\n"
        "Features:\n"
        "💬 AI Chat\n"
        "🧠 Memory\n"
        "🖼️ Image Support\n"
        "🎤 Voice Support\n"
        "📄 Document Support"
    )

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.effective_user.id
    text = update.message.text

    add_message(uid, "user", text)

    messages = [
        {
            "role": "system",
            "content": "You are a smart AI assistant."
        }
    ]

    messages += get_messages(uid)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content

        add_message(uid, "assistant", answer)

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(str(e))

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Image received.\nImage analysis code can be added here."
    )

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎤 Voice received.\nVoice transcription code can be added here."
    )

async def document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Document received.\nPDF/Text reading code can be added here."
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

app.add_handler(MessageHandler(filters.PHOTO, image))

app.add_handler(MessageHandler(filters.VOICE, voice))

app.add_handler(MessageHandler(filters.Document.ALL, document))

print("Bot Started...")

app.run_polling()
