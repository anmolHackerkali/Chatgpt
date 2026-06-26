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
        "🤖 Gemini AI Bot Ready!\n\nSend me any message."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    add_message(user_id, "user", text)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    messages += get_messages(user_id)

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content

        add_message(user_id, "assistant", answer)

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Error:\n{e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Started...")

app.run_polling()