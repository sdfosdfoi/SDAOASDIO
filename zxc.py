import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import time
import random
import threading
import logging
from flask import Flask, request
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = '8356139072:AAFhiu7mSCb431Ewa8-vnwIPVsLW9l46TyA'
bot = telebot.TeleBot(TOKEN)

# Создаём Flask-приложение для обработки webhook
app = Flask(__name__)

# Список случайных уведомлений (короткие фразы, до 2 слов)
messages = [
    "Лабубу голоден!",
    "Хочет играть!",
    "Ему грустно...",
    "Нужен корм!",
    "Скучает по тебе!",
    "Устал играть.",
    "Хочет внимания!",
    "Грустит один...",
    "Готов к приключениям!",
    "Нужен отдых."
]

user_threads = {}  # Словарь для хранения потоков пользователей

def create_play_button():
    logger.info("Создание кнопки Web App")
    markup = InlineKeyboardMarkup()
    play_button = InlineKeyboardButton(
        text="Играть!",
        web_app=WebAppInfo(url="https://labubub-4mj5.vercel.app")
    )
    markup.add(play_button)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    welcome_text = (
        "Привет! Я Лабубу, твой милый виртуальный питомец! 🐾\n"
        "В игре ты можешь заботиться обо мне, кормить, играть и делать меня счастливее! "
        "Открывай сундуки, чтобы выбить редких Лабубу, повышай мой уровень и стань самым крутым в школе! 🏆 "
        "Собирай уникальных питомцев, соревнуйся с друзьями и покажи всем, кто здесь босс! "
        "Я буду напоминать тебе каждые 30 минут, когда мне нужно внимание. 😊 Готов начать?"
    )
    logger.info(f"Отправка приветственного сообщения в чат {chat_id}")
    bot.reply_to(message, welcome_text, reply_markup=create_play_button())
    
    # Если поток уже существует, не создаем новый
    if chat_id not in user_threads:
        def send_notifications():
            while True:
                time.sleep(1800)  # 30 минут в секундах
                notification = random.choice(messages)
                try:
                    bot.send_message(chat_id, notification)
                    logger.info(f"Уведомление отправлено в чат {chat_id}: {notification}")
                except Exception as e:
                    logger.error(f"Ошибка отправки в чат {chat_id}: {e}")
        
        thread = threading.Thread(target=send_notifications, daemon=True)
        thread.start()
        user_threads[chat_id] = thread
        logger.info(f"Запущен поток уведомлений для чата {chat_id}")

# Эндпоинт для обработки webhook
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_json())
    if update:
        bot.process_new_updates([update])
    return '', 200

# Главная страница (для проверки)
@app.route('/')
def index():
    return 'Bot is running!'

# Настройка webhook
def setup_webhook():
    try:
        bot.remove_webhook()
        time.sleep(1)  # Задержка для удаления старого webhook
        webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
        bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook установлен: {webhook_url}")
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")

# Запуск Flask и бота
if __name__ == '__main__':
    logger.info("Бот запускается...")
    setup_webhook()
    port = int(os.getenv('PORT', 5000))  # Render задаёт PORT, по умолчанию 5000
    app.run(host='0.0.0.0', port=port, debug=False)