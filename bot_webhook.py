import os, logging, openai
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

BOT_TOKEN        = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
GPT_MODEL        = "gpt-3.5-turbo"          # или gpt-4o
PORT             = int(os.getenv("PORT", 10000))
BASE_URL         = os.getenv("RENDER_EXTERNAL_URL")  # автоматическая переменная Render  [oai_citation:1‡render.com](https://render.com/docs/environment-variables?utm_source=chatgpt.com)
WEBHOOK_PATH     = f"/webhook/{BOT_TOKEN}"

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

async def ask_gpt(prompt: str) -> str:
    try:
        resp = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        logging.exception("OpenAI error")
        return "⚠️ GPT не ответил."

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я GPT‑бот.")

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.chat.send_action("typing")
    answer = await ask_gpt(update.message.text)
    await update.message.reply_text(answer)

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    public_url = BASE_URL.rstrip("/")        # «https://xxxxx.onrender.com»
    webhook_url = f"{public_url}{WEBHOOK_PATH}"
    logging.info("Webhook URL: %s", webhook_url)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    main()
