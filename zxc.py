import asyncio
import random
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8356139072:AAFhiu7mSCb431Ewa8-vnwIPVsLW9l46TyA"

logging.basicConfig(level=logging.INFO)

MESSAGES = [
    "Лабубу проголодался 🐾🍲",
    "Лабубу хочет играть 🎮🐶",
    "Лабубу скучает 😿",
    "Лабубу загрустил 💔",
    "Лабубу ждёт тебя 🐕✨",
    "Лабубу хочет обнимашек 🤗"
]

chat_ids = set()

# Приветствие
async def start(update: "Update", context: "ContextTypes.DEFAULT_TYPE"):
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
    await update.message.reply_text(greeting, reply_markup=keyboard)

# Отписка
async def stop(update: "Update", context: "ContextTypes.DEFAULT_TYPE"):
    chat_ids.discard(update.effective_chat.id)
    await update.message.reply_text("❌ Ты отписался от уведомлений о Лабубу.")

# Фоновая задача
async def notifier(bot):
    while True:
        if chat_ids:
            msg = random.choice(MESSAGES)
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🎮 Играть", url="https://labubub-4mj5.vercel.app")]]
            )
            for chat_id in chat_ids.copy():
                try:
                    await bot.send_message(chat_id, msg, reply_markup=keyboard)
                except Exception as e:
                    logging.error(e)
        await asyncio.sleep(1800)  # 30 минут

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    # Запускаем фоновую задачу
    asyncio.create_task(notifier(app.bot))

    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
