import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔴 PUT YOUR REAL TOKENS HERE
TELEGRAM_TOKEN = "8543845620:AAEwF0jfkLHhR7DyRm50DxxVbm_7DJtdRFc"
OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "arcee-ai/trinity-large-preview:free",
        "messages": [
            {"role": "user", "content": user_text}
        ],
        "reasoning": {"enabled": True}
    }

    response = requests.post(
        url=OPENROUTER_URL,
        headers=headers,
        data=json.dumps(data)
    )

    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "Error: Could not get response from OpenRouter."

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running with OpenRouter...")
app.run_polling()