from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq
import os

TOKEN: Final ='8671746228:AAGqN6g2ApmGsdm3AmkF2awv1VeGxFrCCEg'
BOT_USERNAME: Final = '@leul_leul_bot'

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
        return '🥸hey there!'

    if 'hi' in processed:
        return 'hey there i am here to help you! tell me what is ur name'

    if 'how are you' in processed:
        return 'i am good how abt you?'

    if 'i am fine i want you to ask you about something' in processed:
        return 'iam happy to see you fine and your wellcom you can ask!'

    if 'hi leul' in processed:
        return 'hi my boy how you doing 😘!'

    if 'i am fine where are you now' in processed:
        return 'in my home dude what are you thinking🤦‍♂️!'

    if 'my name is sena' in processed:
        return 'sena my brother 🥰 fuck which sena you are?'

    if 'my name is habtamu' in processed:
        return 'habte my brother 🥰 how are you? i missed u a lot'

    if 'is this bot created by leul' in processed:
        return 'yes absolutely! he is the owner and the leader of this group🤑'

    return None  # IMPORTANT: means “no match”


# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"User: {text}")

    # 1. try your old rules first
    response = handle_responses(text)

    # 2. if no match → use AI
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
    app.run_polling()