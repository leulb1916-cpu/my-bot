from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq
import os
import os

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = '@leul_leul_bot'
if not TOKEN:
    print("ERROR: BOT_TOKEN is missing!")
    exit()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# AI FUNCTION
def ask_ai(text: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content


# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hellow! Thanks for chatting with me! I am Leul your friend!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("i am here Leul please type something i can respond")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is a custom command bro/sis")


# YOUR OLD LOGIC (kept exactly style)
def handle_responses(text: str) -> str:
    processed = text.lower()

    if 'hellow' in processed:
        return '🥸hey there i am leul here!'

    if 'hi' in processed:
        return 'hey there i am leul here😘 to help you! tell me what is on your mind'

    if 'how are you' in processed:
        return 'i am good how about you?'

    if 'do you know about leul' in processed:
        return 'yes absolutely🥰! he is my father'

    if 'who is leul' in processed:
        return 'leul is my god who manage me!'

    if 'i am fine where are you now' in processed:
        return 'in my home dude what are you thinking🤦‍♂️!'

    if 'who are you' in processed:
        return 'i am leul what 🥰 is on your mind'

    if 'my name is habtamu' in processed:
        return 'habte my brother 🥰 how are you? i missed u a lot'

    if 'who wade you' in processed:
        return 'i am 😒created by leul'

    return None  # IMPORTANT: means “no match”


# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    text = update.message.text
    chat_type = update.effective_chat.type

    print(f"{chat_type}: {text}")

    # ---------- PRIVATE CHAT ----------
    if chat_type == "private":
        response = handle_responses(text)

        if response is None:
            response = ask_ai(text)

        await update.message.reply_text(response)
        return

    # ---------- GROUP / SUPERGROUP ----------
    if chat_type in ["group", "supergroup"]:

        # Ignore messages that don't mention the bot
        if BOT_USERNAME.lower() not in text.lower():
            return

        # Remove the @mention
        text = text.replace(BOT_USERNAME, "").strip()

        # If the user only typed "@leul_leul_bot"
        if text == "":
            await update.message.reply_text("Hi! i leul😊 How can I help?")
            return

        # Check your custom replies first
        response = handle_responses(text)

        # Otherwise ask Groq AI
        if response is None:
            response = ask_ai(text)

        await update.message.reply_text(response)

# ERROR
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")


# MAIN
if __name__ == "__main__":
    print("Bot starting...")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Polling...")
    app.run_polling(drop_pending_updates=True)