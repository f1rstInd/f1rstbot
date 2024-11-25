import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Azure OpenAI settings
OPENAI_API_KEY = "YOUR_AZURE_OPENAI_API_KEY"
OPENAI_ENDPOINT = "https://YOUR_AZURE_OPENAI_ENDPOINT/openai/deployments/YOUR_DEPLOYMENT_NAME/completions?api-version=2023-03-15-preview"
HEADERS = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}

# Telegram Bot Token
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

def chat_with_openai(prompt):
    payload = {
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
    }
    response = requests.post(OPENAI_ENDPOINT, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text").strip()
    else:
        return "Sorry, there was an issue connecting to OpenAI."

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your AI bot. Ask me anything!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    ai_response = chat_with_openai(user_message)
    update.message.reply_text(ai_response)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
