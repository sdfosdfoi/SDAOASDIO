import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "ТВОЙ_ТОКЕН"

MESSAGES = [
    "Лабубу проголодался 🐾🍲",
    "Лабубу хочет играть 🎮🐶",
    "Лабубу скучает 😿",
    "Лабубу загрустил 💔",
    "Лабубу ждёт тебя 🐕✨",
    "Лабубу хочет обнимашек 🤗"
]

logging.basicConfig(level=logging.INFO)

chat_ids = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_ids.add(update.effective_chat.id)

    greeting = (
        "Привет, друг! 🐶✨\n\n"
        "Я — бот Лабубу 💖\n"
        "Буду каждые 30 минут напоминать тебе, когда нужно поиграть, покормить "
        "или просто обнять Лабубу 🐾💞\n\n"
        "Нажимай кнопку 🎮 и заходи в игру!"
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🎮 Играть", url="https://labubub-4mj5.vercel.app")]]
    )

    await update.message.reply_text(greeting, reply_markup=keyboard, parse_mode="Markdown")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in chat_ids:
        chat_ids.remove(update.effective_chat.id)
        await update.message.reply_text("❌ Ты отписался от уведомлений о Лабубу.")
    else:
        await update.message.reply_text("ℹ️ Ты ещё не был подписан.")

async def notifier(app: Application):
    while True:
        if chat_ids:
            msg = random.choice(MESSAGES)
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🎮 Играть", url="https://labubub-4mj5.vercel.app")]]
            )
            for chat_id in list(chat_ids):
                try:
                    await app.bot.send_message(chat_id, msg, reply_markup=keyboard)
                except Exception as e:
                    logging.error(e)
        await asyncio.sleep(1800)  # 30 минут

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    # Запускаем задачу после старта
    async def on_startup(app: Application):
        app.create_task(notifier(app))

    app.run_polling(on_startup=on_startup)

if __name__ == "__main__":
    main()
