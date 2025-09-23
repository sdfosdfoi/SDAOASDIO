import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import threading

# Токен бота
TOKEN = '8356139072:AAFhiu7mSCb431Ewa8-vnwIPVsLW9l46TyA'
bot = telebot.TeleBot(TOKEN)

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
    # Создаём инлайн-кнопку для открытия игры как Telegram Web App
    markup = InlineKeyboardMarkup()
    play_button = InlineKeyboardButton(
        text="Играть!", 
        web_app={"url": "https://labubub-4mj5.vercel.app"}  # Открывает игру в Telegram WebView
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
    # Отправляем приветствие с кнопкой "Играть!"
    bot.reply_to(message, welcome_text, reply_markup=create_play_button())
    
    # Если поток уже существует, не создаем новый
    if chat_id not in user_threads:
        def send_notifications():
            while True:
                time.sleep(1800)  # 30 минут в секундах
                notification = random.choice(messages)
                try:
                    bot.send_message(chat_id, notification)
                except Exception as e:
                    print(f"Ошибка отправки: {e}")
        
        thread = threading.Thread(target=send_notifications, daemon=True)
        thread.start()
        user_threads[chat_id] = thread

# Автоматическое удаление webhook перед запуском polling
try:
    bot.delete_webhook()  # Удаляем webhook для корректной работы polling
    print("Webhook удалён успешно.")
except Exception as e:
    print(f"Ошибка при удалении webhook: {e}")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)