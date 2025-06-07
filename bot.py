import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ВСТАВЬ СВОИ КЛЮЧИ
TELEGRAM_BOT_TOKEN = "7865133019:AAEp6SAXei7l0TSF3fAnaVn_9FPrKURbWe0"
OPENAI_API_KEY = "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"

# Настройка GPT
openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-3.5-turbo"  # или "gpt-4o", если доступен

# Генерация ответа от GPT
async def ask_gpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        return "⚠️ Произошла ошибка при обращении к GPT."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я GPT-бот. Напиши мне что-нибудь — я отвечу 🤖")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.chat.send_action("typing")
    response = await ask_gpt(user_message)
    await update.message.reply_text(response)

# Запуск бота
def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
