import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo"

openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка GPT: {e}")
        return "⚠️ GPT не ответил."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я GPT-бот. Напиши мне что-нибудь!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.chat.send_action("typing")
    reply = await ask_gpt(text)
    await update.message.reply_text(reply)

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
